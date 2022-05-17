# Summary
This project is designed to follow the format put forth by the [public RADS web archive by PixelButts](https://archive.org/details/league-of-legends-rads-patch-system-2010-2019).

Given a realm directory from the archive, this project will compile all of the project files for a given solution.

# Usage:
You must extract the realm you want from the archive first as well as the file hash list.

## Command:
`python -m radscomp RADS_FILEHASHES REALM SOLUTION_NAME VERSION TARGET_DIR`
* **RADS_FILEHASHES** -- path to the text file containing file hashes of all realms and versions.
  * ex: `"RADS_Hashes_MD5.txt"`
* **REALM_DIR** -- directory of the realm containing solution and project files.
  * ex: `"path/to/live"`
* **SOLUTION_NAME** -- name of the solution to target.
  * ex: `"lol_game_client_sln"`
* **VERSION** -- version of the solution to target.
  * ex: `"0.0.1.68"`
* **TARGET_DIR** -- directory to compile the files into. Must end with the parent directory being the realm name.
  * ex: `"C:/Users/admin/Desktop/RADS_Exports"`
  
