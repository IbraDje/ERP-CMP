# ERP-CMP
EquiRectangular - CubeMap Projections

<hr>
<h2>cmpToErp :</h2> <pre>getErpPatch(campFaces)</pre>
<h3>CubeMap Projection to EquiRectangular Projection</h3>
  <b>Parameters:</b>
  <ul>
  <li><code><var>cmpFaces</var></code> : CubeMap Projected Faces (OpenCV BGR Format):
      front, right, back, left, top, bottom
      with shape : [6, H, W, 3]</li></ul>
  <b>Returns:</b><ul>
      <li><code><var>erpPatch</var></code> : Equirectangular Projected Image
      with shape : <code><var>[H, W*2, 3]</var></code></li>
  </ul>

<hr>
<h2>erpToCmp :</h2> <pre>getCmpFaces(erpPatch, H=None, W=None)</pre>
<h3>EquiRectangular Projection to CubeMap Projection Function</h3>
  <b>Parameters:</b>
  <ul>
      <li><code><var>erpPatch</var></code> : Equirectangular Projected Image (OpenCV BGR Format)</li>
      <li><code><var>H</var></code> : Height of CMP Faces (default : <code><var>erpPatch.shape[0] // 2</var></code>)</li>
      <li><code><var>W</var></code> : Width of CMP Faces (default : <code><var>erpPatch.shape[1] // 4</var></code>)</b></li>
  </ul>
  <b>Returns:</b>
  <ul>
      <li><code><var>cmpFaces</var></code> : CubeMap Projected Faces:
      front, right, back, left, top, bottom
      with shape : <code><var>[6, H, W, 3]</var></code></li>
  </ul>
<hr>
<h2> References </h2>
  <ol>
    <li>https://github.com/rayryeng/cubic2equi/blob/master/cubic2equi.m</li>
    <li>https://github.com/pepepor123/equirectangular-to-cubemap</li>
  </ol>
