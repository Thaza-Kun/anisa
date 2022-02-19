@ECHO OFF
SET filename=%1
SET scenename=%2
%~dp0.venv\Scripts\manim.exe -pql %filename% %scenename%