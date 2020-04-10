# ERP-CMP
EquiRectangular - CubeMap Projections

<hr>
<h1>cmpToErp :</h1> `getErpPatch(campFaces)`
<h3>CubeMap Projection to EquiRectangular Projection</h3>
  <b>Parameters:</b>
  <ul>
      <li>`cmpFaces` : CubeMap Projected Faces (OpenCV BGR Format):
      front, right, back, left, top, bottom
      with shape : [6, H, W, 3]</li></ul>
  <b>Returns:</b><ul>
      <li>`erpPatch` : Equirectangular Projected Image
      with shape : [H, W*2, 3]</li>
  </ul>

<hr>
<h1>erpToCmp :</h1> getCmpFaces(erpPatch, H=None, W=None)
<h3>EquiRectangular Projection to CubeMap Projection Function</h3>
  <b>Parameters:</b>
  <ul>
      <li><b>erpPatch :</b> Equirectangular Projected Image (OpenCV BGR Format)</li>
      <li><b>H :</b> Height of CMP Faces (default : patch.shape[0] // 2)</li>
      <li><b>W :</b> Width of CMP Faces (default : patch.shape[1] // 4)</b></li>
  </ul>
  <b>Returns:</b>
  <ul>
      <li><b>cmpFaces :</b> CubeMap Projected Faces:
      front, right, back, left, top, bottom
      with shape : [6, H, W, 3]</li>
  </ul>

<h1> References </h1>
  <ol>
    <li>https://github.com/rayryeng/cubic2equi/blob/master/cubic2equi.m</li>
    <li>https://github.com/pepepor123/equirectangular-to-cubemap</li>
  </ol>
