#version 330

// axis vertex attributes (position and colour)
layout (location=0) in vec3 apos;
layout (location=1) in vec3 acol;

// transform axis matrices
uniform mat4 view;
uniform mat4 proj;

// pass colour to fragment shader
out vec3 vcol;

void main()
{
    // no model as axis constant transform
    gl_Position = proj * view * vec4(apos.x, apos.y, apos.z, 1.0);
    vcol = acol;
}