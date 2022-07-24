#version 330

// path vertex attribute position
layout (location=0) in vec3 apos;

// paths transform matrices
uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

void main()
{
    gl_Position = proj * view * vec4(apos.x, apos.y, apos.z, 1.0);
}