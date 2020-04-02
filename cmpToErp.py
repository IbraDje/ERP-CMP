import numpy as np


def getErpPatch(cmpFaces):
    '''
    <h3>CubeMap Projection to EquiRectangular Projection</h3>
    Inspired from https://github.com/rayryeng/cubic2equi/blob/master/cubic2equi.m
    <b>Parameters:</b><ul>
        <li><b>cmpFaces :</b> CubeMap Projected Faces (OpenCV BGR Format):
        front, right, back, left, top, bottom
        with shape : [6, H, W, 3]</li></ul>
    <b>Returns:</b><ul>
        <li><b>erpPatch :</b> Equirectangular Projected Image
        with shape : [H, W*2, 3]</li></ul>
    '''
    height = cmpFaces.shape[1]
    width = 2 * cmpFaces.shape[2]

    faceXNeg = 4  # Front
    faceZNeg = 1  # Right
    faceXPos = 5  # Back
    faceZPos = 0  # Left
    faceYPos = 2  # Top
    faceYNeg = 3  # Bottom

    stackedImages = [faceXNeg, faceZNeg,
                     faceXPos, faceZPos, faceYPos, faceYNeg]

    facesB = np.ndarray(
        (cmpFaces.shape[1], cmpFaces.shape[2], 6), dtype=cmpFaces.dtype)
    facesG = np.copy(facesB)
    facesR = np.copy(facesB)

    for i, face in enumerate(cmpFaces):
        facesB[:, :, stackedImages[i]] = face[:, :, 0]
        facesG[:, :, stackedImages[i]] = face[:, :, 1]
        facesR[:, :, stackedImages[i]] = face[:, :, 2]

    X, Y = np.meshgrid(np.linspace(0, width, width, endpoint=False),
                       np.linspace(0, height, height, endpoint=False))

    Y = 2*Y/height - 1
    X = 2*X/width - 1

    sphereTheta = X*np.pi
    spherePhi = Y*np.pi/2

    texX = np.cos(spherePhi)*np.cos(sphereTheta)
    texY = np.sin(spherePhi)
    texZ = np.cos(spherePhi)*np.sin(sphereTheta)

    comp = np.stack((texX, texY, texZ), axis=2)
    ind = np.argmax(np.abs(comp), axis=2)
    maxVal = np.zeros(shape=ind.shape)
    maxVal[ind == 0] = texX[ind == 0]
    maxVal[ind == 1] = texY[ind == 1]
    maxVal[ind == 2] = texZ[ind == 2]

    getFace = -1*np.ones(shape=maxVal.shape)

    # Front
    ind = np.logical_and(np.less(np.abs(maxVal - texX),
                                 0.00001), np.greater_equal(texX, 0))
    getFace[ind] = faceXNeg

    # Right
    ind = np.logical_and(np.less(np.abs(maxVal - texZ),
                                 0.00001), np.greater_equal(texZ, 0))
    getFace[ind] = faceZNeg

    # Back
    ind = np.logical_and(
        np.less(np.abs(maxVal - texX), 0.00001), np.less(texX, 0))
    getFace[ind] = faceXPos

    # Left
    ind = np.logical_and(
        np.less(np.abs(maxVal - texZ), 0.00001), np.less(texZ, 0))
    getFace[ind] = faceZPos

    # Top
    ind = np.logical_and(
        np.less(np.abs(maxVal - texY), 0.00001), np.less(texY, 0))
    getFace[ind] = faceYPos

    # Bottom
    ind = np.logical_and(np.less(np.abs(maxVal - texY),
                                 0.00001), np.greater_equal(texY, 0))
    getFace[ind] = faceYNeg

    rawX = -1*np.ones(shape=maxVal.shape)
    rawY = np.copy(rawX)
    rawZ = np.copy(rawX)

    # Front
    ind = getFace == faceXNeg
    rawX[ind] = texZ[ind]
    rawY[ind] = texY[ind]
    rawZ[ind] = texX[ind]

    # Right
    ind = getFace == faceZNeg
    rawX[ind] = -texX[ind]
    rawY[ind] = texY[ind]
    rawZ[ind] = texZ[ind]

    # Back
    ind = getFace == faceXPos
    rawX[ind] = -texZ[ind]
    rawY[ind] = texY[ind]
    rawZ[ind] = texX[ind]

    # Left
    ind = getFace == faceZPos
    rawX[ind] = texX[ind]
    rawY[ind] = texY[ind]
    rawZ[ind] = texZ[ind]

    # Top
    ind = getFace == faceYPos
    rawX[ind] = texZ[ind]
    rawY[ind] = texX[ind]
    rawZ[ind] = texY[ind]

    # Bottom
    ind = getFace == faceYNeg
    rawX[ind] = texZ[ind]
    rawY[ind] = -texX[ind]
    rawZ[ind] = texY[ind]

    rawCoords = np.stack((rawX, rawY, rawZ), axis=2)

    cubeCoordsX = ((rawCoords[:, :, 0] / np.abs(rawCoords[:, :, 2])) + 1) / 2
    cubeCoordsY = ((rawCoords[:, :, 1] / np.abs(rawCoords[:, :, 2])) + 1) / 2
    cubeCoords = np.stack((cubeCoordsX, cubeCoordsY), axis=2)

    normalizedX = np.around(cubeCoords[:, :, 0] * height)
    normalizedY = np.around(cubeCoords[:, :, 1] * height)

    normalizedX = np.clip(normalizedX, 0, height-1)
    normalizedY = np.clip(normalizedY, 0, height-1)

    normalizedCoords = np.stack(
        (normalizedX, normalizedY), axis=2).astype(np.int32)

    out = np.zeros(shape=(maxVal.shape[0], maxVal.shape[1], 3), dtype=np.uint8)

    out[:, :, 0] = facesB[normalizedCoords[:, :, 1],
                          normalizedCoords[:, :, 0], getFace.astype(np.int32)]
    out[:, :, 1] = facesG[normalizedCoords[:, :, 1],
                          normalizedCoords[:, :, 0], getFace.astype(np.int32)]
    out[:, :, 2] = facesR[normalizedCoords[:, :, 1],
                          normalizedCoords[:, :, 0], getFace.astype(np.int32)]

    return out


if __name__ == '__main__':
    import cv2
    from matplotlib import pyplot as plt

    patchName = 'patch_1'
    cmpFaces = np.ndarray((6, 1250, 1250, 3), dtype=np.uint8)

    for i in range(6):
        cmpFaces[i] = cv2.imread(f'./faces/{patchName}_face_{i+1}.jpg',
                                 cv2.IMREAD_COLOR)

    erpPatch = getErpPatch(cmpFaces).astype(np.uint8)

    faces = ['front', 'right', 'back', 'left', 'top', 'bottom']

    plt.figure(num='CubeMap Faces', figsize=(15, 15))
    for i, cmpFace in enumerate(cmpFaces):
        cmpFace = cv2.cvtColor(cmpFace, cv2.COLOR_BGR2RGB)
        plt.subplot(2, 3, i+1)
        plt.axis('off')
        plt.imshow(cmpFace)
        plt.title(f'{faces[i]} face')
    plt.show()

    plt.figure(num='Resulted EquiRectangular Projected Image', figsize=(15, 15))
    plt.axis('off')
    erpPatch = cv2.cvtColor(erpPatch, cv2.COLOR_BGR2RGB)
    plt.imshow(erpPatch)
    plt.title('Resulted EquiRectangular Projected Image')
    plt.show()
