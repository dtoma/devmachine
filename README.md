# Dev Machine

Setup a development environment in a few seconds.

---

Requirements:

- [vagrant](https://www.vagrantup.com/)
- python 3.x
- python [requests](http://docs.python-requests.org/en/latest/)

---

- [Available OSs](https://github.com/dtoma/ansible-playbooks)
- [Available roles](https://github.com/dtoma/vagrantfiles)

---

Usage:

`dev [OS]/[version] [packages...]`

Example:

`dev ubuntu/trusty64 haskell-stack`

---

To Do:

- [ ] Add an option to list available packages
- [ ] Proper distribution as a standalone command
- [ ] Handle roles with template dependencies
