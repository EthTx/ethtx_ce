# New Semantics
As part of community, you can create new semantics to help decode transactions. 

## Structure
 
In `ethtx_ce/semantics` you have to create new `file` or `subdirectory & file`.
It does not matter at all, because code automatically scans all subdirectories, but we take
care of proper grouping and oder.

## Implementation
* import: 
  ```python 
  from ethtx_ce.semantics.base import Base
  ```
* create new class:
  ```python 
  class YourClass(Base):
    code_hash = "your code hash"
    contract_semantics = {"your logic": "here"}
  ```

As you can see, it is very simple. You have always to inherit from `Base` class.
In other case new `Semantic` will not be injected to code. This mechanism ensures the
correctness of creating semantics.

---

# Local Development
This repository contains 2 basic applications: `frontend` & `backend`.  
It is easy to manage, and you can easily add new local application(s).

## Basic structure
Application is based on ![blueprints](https://flask.palletsprojects.com/en/1.1.x/blueprints/).

New extension requires:
 - new Python Package in ![ethtx_ce](ethtx_ce) subdirectory.
- `create_app` function (created in new package in `init` file) which returns `Flask` object by calling ![app factory](ethtx_ce/factory.py) file.
- calling a function above in a `run.py` file with assigned url prefix.

These simple steps allow you to add new extension and integrate with entire application.

---

# Community Roles

While these developer community roles are informal,
there are many ways to get involved with the EthTx community, such as:
- co-creating the community version by developing and improving the current components 
- using the solution in other projects
- adding new features that will make using the community version even better 

We will be involved in each of these steps.