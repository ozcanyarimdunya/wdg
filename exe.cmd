rd /s /q dist build
del "Word Document Generator.spec"

pyinstaller ^
--name="Word Document Generator" ^
--icon="assets\\icons\\icons.ico" ^
--windowed ^
--onefile ^
--add-data="assets;assets" ^
--hidden-import="textract.parsers.docx_parser" start.py
