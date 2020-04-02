import numpy as np
from scipy import ndimage


def getCmpFaces(erpPatch, H=None, W=None):
    '''
    <h3>EquiRectangular Projection to CubeMap Projection Function</h3>
    <b>Parameters:</b><ul>
        <li><b>erpPatch :</b> Equirectangular Projected Image (OpenCV BGR Format)</li>
        <li><b>H :</b> Height of CMP Faces (default : patch.shape[0] // 2)</li>
        <li><b>W :</b> Width of CMP Faces (default : patch.shape[1] // 4)</b></li></ul>
    <b>Returns:</b><ul>
        <li><b>cmpFaces :</b> CubeMap Projected Faces:
        front, right, back, left, top, bottom
        with shape : [6, H, W, 3]</li></ul>
    '''
    V = [0, 0, 0, 0, -np.pi/2, np.pi/2]
    U = [0, np.pi/2, np.pi, -np.pi/2, 0, 0]
    fov = np.pi/2

    if H is None:
        H = erpPatch.shape[0] // 2
    if W is None:
        W = erpPatch.shape[1] // 4

    cmpFaces = np.ndarray((6, H, W, 3))

    for i, (u, v) in enumerate(zip(U, V)):
        cmpFaces[i] = eqToPers(erpPatch, fov, u, v, H, W)

    return cmpFaces


def genXYZ(fov, u, v, outH, outW):
    ''' Source : https://github.com/pepepor123/equirectangular-to-cubemap '''
    out = np.ones((outH, outW, 3), np.float32)

    xRng = np.linspace(-np.tan(fov / 2), np.tan(fov / 2),
                       num=outW, dtype=np.float32)
    yRng = np.linspace(-np.tan(fov / 2), np.tan(fov / 2),
                       num=outH, dtype=np.float32)

    out[:, :, :2] = np.stack(np.meshgrid(xRng, -yRng), -1)
    Rx = np.array([[1, 0, 0], [0, np.cos(v), -np.sin(v)],
                   [0, np.sin(v), np.cos(v)]])
    Ry = np.array([[np.cos(u), 0, np.sin(u)], [
                  0, 1, 0], [-np.sin(u), 0, np.cos(u)]])

    R = np.dot(Ry, Rx)
    return out.dot(R.T)


def xyzToUV(xyz):
    ''' Source : https://github.com/pepepor123/equirectangular-to-cubemap '''
    x, y, z = np.split(xyz, 3, axis=-1)
    u = np.arctan2(x, z)
    c = np.sqrt(x ** 2 + z ** 2)
    v = np.arctan2(y, c)
    return np.concatenate([u, v], axis=-1)


def uvToXY(uv, eqH, eqW):
    ''' Source : https://github.com/pepepor123/equirectangular-to-cubemap '''
    u, v = np.split(uv, 2, axis=-1)
    X = (u / (2 * np.pi) + 0.5) * eqW - 0.5
    Y = (-v / np.pi + 0.5) * eqH - 0.5
    return np.concatenate([X, Y], axis=-1)


def eqToPers(eqimg, fov, u, v, outH, outW):
    ''' Source : https://github.com/pepepor123/equirectangular-to-cubemap '''
    xyz = genXYZ(fov, u, v, outH, outW)
    uv = xyzToUV(xyz)

    eq_h, eq_w = eqimg.shape[:2]
    XY = uvToXY(uv, eq_h, eq_w)

    X, Y = np.split(XY, 2, axis=-1)
    X = np.reshape(X, (outH, outW))
    Y = np.reshape(Y, (outH, outW))

    mc0 = ndimage.map_coordinates(eqimg[:, :, 0], [Y, X])  # channel: B
    mc1 = ndimage.map_coordinates(eqimg[:, :, 1], [Y, X])  # channel: G
    mc2 = ndimage.map_coordinates(eqimg[:, :, 2], [Y, X])  # channel: R

    output = np.stack([mc0, mc1, mc2], axis=-1)
    return output


if __name__ == '__main__':
    import cv2
    from matplotlib import image as mpimg, pyplot as plt

    patchName = 'patch_1'

    erpPatch = cv2.imread(f'./patches/{patchName}.jpg', cv2.IMREAD_COLOR)

    cmpFaces = getCmpFaces(erpPatch).astype(np.uint8)

    faces = ['front', 'right', 'back', 'left', 'top', 'bottom']

    plt.figure(num="Resulted CubeMap Faces", figsize=(15, 15))
    for i, cmpFace in enumerate(cmpFaces):
        cmpFace = cv2.cvtColor(cmpFace, cv2.COLOR_BGR2RGB)
        plt.subplot(2, 3, i+1)
        plt.axis('off')
        plt.imshow(cmpFace)
        plt.title(f'{faces[i]} face')
        mpimg.imsave(f'./faces/{patchName}_face_{i+1}.jpg', cmpFace)
    plt.show()
