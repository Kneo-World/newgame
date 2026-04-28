import zipfile
import xml.etree.ElementTree as ET
import os

def convert_catrobat(file_path):
    # This script logic is what powers this web app!
    # It uses zipfile to unpack and ElementTree to find objects.
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall('extracted_project')
    
    tree = ET.parse('extracted_project/code.xml')
    root = tree.getroot()
    
    print(f"Project Name: {root.find('.//programName').text}")
    print("Objects found:")
    for obj in root.findall('.//object'):
        print(f"- {obj.find('name').text}")

if __name__ == "__main__":
    # convert_catrobat('project.catrobat')
    print("Skibidi Converter Core Ready!")