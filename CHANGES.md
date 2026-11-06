**Version 2.0.0:**
- Date: November 6th, 2026
- Author: Robert Burns
- Changes:
    - Rewrote KeyMapper to keep its data in the dict alone. Values set with update(), setdefault(), or any other dict method are now reachable by path, and delimiter is no longer stored as a key in your data
    - Breaking: a missing key raises KeyError, as a dict does; get(key, default) returns a default
    - Breaking: removed attribute access, which answered None for any name and made hasattr() always true
    - Breaking: removed the schema option
    - Writing to a path creates the mappings it needs
    - Paths walk lists and tuples by index, negative indexes included, and find falsy values such as 0 and ""
    - Path parts match string keys first, then integer keys, so {"0": ...} and {0: ...} both work
    - Tuple paths, such as km["build", "tag.name"], keep each part whole; a key that exists as written always wins
    - Sets are no longer indexed, since they have no order
    - Added pytest tests, GitHub Actions CI on Python 3.11 to 3.15, pyproject.toml, and type information (py.typed); Python 3.11 or newer is required
    - Fixed the project links, which pointed to GitLab

---


**Version 1.0.2:**
- Date: December 9th, 2019
- Author: Robert Burns
- Changes:
    - Fixed regex match bug when searching for numbers
    - Added \_\_repr\_\_
    - Added \_\_str\_\_
    - Renamed mapper to \_\_mapper\_\_
    
---

**Version 1.0.1:**
- Date: March 18th, 2019
- Author: Robert Burns
- Changes:
    - Fixed bug when calling __getitem__ from a list
    - Implemented __setitem__ calls regardless of the value being a dict, or some type of iterable
    - Removed the replace method searching for the bracket characters, when declaring an iterable of some type in the key declaration
    - Small optimizations

---

**Version 1.0.0:**
- Date: May 11th, 2018
- Author: Robert Burns
- Changes:
    - Added keymapper/
    - Added keymapper/__init__.py
    - Added tests/
    - Added tests/__init__.py
    - Added tests/test_km.py
    - Added CHNAGES.md
    - Added .gitignore
    - Added License.txt
    - Added MANIFEST.in
    - Added README.md
    - Added setup.cfg
    - Added setup.py