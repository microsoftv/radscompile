"""Usage:
  python -m radscompile <REALM_DIR> <SOLUTION_NAME> <VERSION> <TARGET_DIR>

Arguments:
  <REALM_DIR> -- directory of the realm containing solution and project files.
  <SOLUTION_NAME> -- name of the solution to target.
  <VERSION> -- version of the solution to target.
  <TARGET_DIR> -- directory to compile the files into.
"""

import os
import shutil
import sys
import manifestparse.manifestparse as parser

# realm index map
REALMS = {
    "esportstmnt01": 1,
    "esportstmnt02": 2,
    "esportstmnt03": 3,
    "esportstmnt04": 4,
    "esportstmnt05": 5,
    "esportstmnt06": 6,
    "fluttershtaging": 7,
    "fluttershtagingMac": 8,
    "fra1tmnt2": 9,
    "fratr1": 10,
    "KoreaLive": 11,
    "KoreaTournament": 12,
    "KR_CBT": 13,
    "live": 14,
    "Maclive": 15,
    "macpbe": 16,
    "pax2damax": 17,
    "PaxEast2012": 18,
    "pbe": 19,
    "ptr": 20,
    "satr1": 21,
    "testrealm": 22,
    "tmnt": 23,
    "tmnt2": 24,
    "twtr1": 25
}

# empty dictionary of project versions
VERSION_LIST = dict()

def compile_directory(directory, parent_dir, realm, project, version, target_dir):
    print("Compiling directory: %s with files: %i" % (directory.name, len(directory.files)))

    directory_path = parent_dir + directory.name + '\\'

    for file in directory.files:
        # convert int version to string
        file_version = '0.0.0.' + str(file.version)
        if (file.version > 255):
            file_version = '0.0.1.' + str(file.version - 256)

        copy_path = sys.argv[1] + '\\projects\\' + project + '\\releases\\' + file_version + '\\files' + directory_path + file.name
        paste_path = target_dir + '\\' + realm + '\\projects\\' + project + '\\releases\\' + version + directory_path + file.name

        print("Copy file: %s" % paste_path)

        if not os.path.exists(os.path.dirname(paste_path)):
            os.makedirs(os.path.dirname(paste_path))
        shutil.copy(copy_path, paste_path)
    
    for subdirectory in directory.subDirectories:
        compile_directory(subdirectory, directory_path, realm, project, version, target_dir)


def compile_files(realm, project, version, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    project_path = sys.argv[1] + '\\projects\\' + project + '\\releases\\' + version

    if (not os.path.exists(project_path)):
        print("Invalid version %s for project %s" % (version, project))
        print(__doc__)
        sys.exit(1)
    
    # get project manifest
    project_manifest = parser.ReleaseManifestFile(project_path + '\\releasemanifest')
    
    for directory in project_manifest.mainDirectories:
        compile_directory(directory, '', realm, project, version, target_dir)

    print("Finished!")

def get_realm_projects(file_hashes, realm):
    print("Reading file hashes from %s" % file_hashes)
    # open text file
    with open(file_hashes, 'r') as f:
        for line in f:
            # skip if line has no slashes
            if '/' not in line:
                continue
            # split line
            line_split = line.split('/')
            # try get realm
            try:
                temprealm = line_split[2]
            except:
                continue
            # skip if not matching realm
            if (temprealm != realm):
                continue
            # try get project
            try:
                project = line_split[4]
            except:
                continue
            # try get version
            try:
                version = line_split[6]
            except:
                continue
            # yield project and version
            yield project, version

def read_manifest(solution_path):
    # open manifest file
    with open(solution_path + "/solutionmanifest", 'r') as f:
        project = ""
        version = ""
        skip = False
        for line in f:
            if (skip):
                skip = False
                continue
            if ('.' not in line):
                if (' ' in line or 'sln' in line):
                    skip = True
                    continue
                project = line.strip()
            else:
                version = line.strip()
            # yield if project and version are not empty
            if (project and version):
                yield project, version
                # empty project and version
                project = ""
                version = ""

def main():

    if len(sys.argv) not in (2, 3, 4, 5):
        print("Invalid number of arguments.")
        print(__doc__)
        sys.exit(1)

    if len(sys.argv) >= 4:
        # get realm name from end of path
        realm = os.path.basename(os.path.normpath(sys.argv[1]))

        # curr_project = ""
        # versions = []
        # # fill version list
        # for project, version in get_realm_projects(sys.argv[1], realm):
        #     if (project != curr_project):
        #         if (len(versions) > 0):
        #             VERSION_LIST[curr_project] = versions
        #         versions = []
        #         VERSION_LIST.update({project: []})
        #         curr_project = project
        #     if ('.' in version and version not in versions):
        #         versions.append(version)

        if realm not in REALMS:
            print("Invalid realm %s" % realm)
            print(__doc__)
            sys.exit(1)
        version = sys.argv[3]
        solution_path = sys.argv[1] + '\\solutions\\' + sys.argv[2] + '\\releases\\' + version
        if not os.path.exists(solution_path):
            print("Invalid version %s for realm %s" % (version, realm))
            print(__doc__)
            sys.exit(1)
        print("Compiling %s version %s for %s" % (realm, version, sys.argv[2]))
        for project, version in read_manifest(solution_path):
            compile_files(realm, project, version, sys.argv[4])
    else:
        print("Invalid arguments given for realm/version.")
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()