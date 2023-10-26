import os

current_directory = os.getcwd()
print(current_directory)
files = os.listdir(current_directory+"/Articles scientifiques")
if not os.path.exists("resume"):
  os.mkdir("resume")

for file in files:
    print(file)
    new_file_name = os.path.join("resume", "resume_texte :{file}.txt".format(file=file))
    new_file = open(new_file_name, "w")
    pdf_name=file.replace(" ", "_")
    pdf_name=pdf_name.replace("-", "_")
    new_file.write(pdf_name)
