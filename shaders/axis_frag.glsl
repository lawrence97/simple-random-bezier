#version 330

// colour from vertex shader
in vec3 vcol;   

// final
out vec4 col;

void main()
{
    col = vec4(vcol, 0.7);
}