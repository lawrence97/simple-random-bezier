## Random bezier curve

Generates a number of successive random 3d quadratic bezier curves and traces their path.

Scene is drawn with OpenGL. Some limited options/settings for the curve and view.

---

Arc end points $p_0$ and $p_1$ 

Control point $p_c$ in **orange** 

![demo](/images/demo.gif)
$b_n$ are the lines which are linearly interpolated over.

$t [0:1]$

$b_0$ : $(1-t)p_0 + tp_c$ 

$b_0$ : $(1-t)p_c + tp_1$

curve : $(1-t)b_0 + tb_1$

quadratic form :  $(1-t)^2 p_0 + 2t(1-t)p_c + p_1t^2$

---

### Examples


- Quadratic beizer curve.

![demo](/images/bezier.png)



- Showing segments of many arcs which curve is tracing along.

![demo](/images/example.png)

---