<h1 align='center' style="border-bottom: none">
  EthTx Community Edition
</h1>
<br/>
<p align="center">
    <em>Community version of EthTx transaction decoder</em>
</p>
<p align="center">
<a target="_blank">
    <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Python">
</a>
<a target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">
</a>
<a target="_blank">
    <img src="https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github" alt="OpenSource">
</a>
<a target="_blank">
    <img src="https://img.shields.io/github/license/Naereen/StrapDown.js.svg" alt="Mit">
</a>
<a target="_blank">
    <img src="https://github.com/EthTx/ethtx_ce/actions/workflows/deploy.yml/badge.svg" alt="Staging pipeline">
</a>
</p>

---

# Local environment

For local instance, you need few things:

0. Depending on your distribution, install: docker, docker-compose, python3-pip, pipenv
1. mongoDB - to set it up for the first time, execute this command: `make populate-db`. This will init db with seed
   provided in repository. After this, if mongo is not running you can raise it with `make run-database`
2. pipenv - to create virtual env run command `pipenv install`, this should create venv for this project with all python
   dependencies.

After this, if you want to run any command inside this env, use `pipenv run` or `pipenv shell`.

To run flask server localy, use `make run-local` command, this will setup new server on host 0.0.0.0 port 5000

# .env file

For proper functioning, `.env` file is required containing all database and 3rd party providers configuration.
`.env.sample` file is provided in repository with default values and should be good to use if nothing else was changed.

Parameters `[CHAIN_ID]_NODE_URL` should hold valid urls to ethereum nodes; Parameter `ETHERSCAN_KEY` should be equal to
Etherscan API key assigned to user.

For docker container, values should be placed in `.env_docker` file since urls for database are differrent than normal
instance

# API

The EthTx APIs are provided as a community service and without warranty, so please use what you need and no more. We
support `GET` requests.

* **Decode transaction**

  Returns decoded EthTx transaction, based on `chain_id` and transaction hash `tx_hash`

    * **URL**
      ```shell
      /api/transactions/CHAIN_ID/TX_HASH
      ```
    * **Method**  
      `GET`
    * **Authorization**
        * Required:  
          header: `x-api-key=[string]` **OR** query parameter: `api_key=[string]`
    * **URL Params**
        * Required: `chain_id=[string]`,`tx_hash=[string]`
    * **Example**
      ```shell
      curl --location --request GET 'http://0.0.0.0:5000/api/transactions/dsad/asd' \
      --header 'x-api-key: 05a2212d-9985-48d2-b54f-0fbc5ba28766'
      ```


* **Get Raw Semantic**

  Returns raw semantic based on `chain_id` and sender/receiver `address`

    * **URL**
      ```shell
      /api/semantics/CHAIN_ID/ADDRESS
      ```
    * **Method**  
      `GET`
    * **Authorization**
        * Required:  
          header: `x-api-key=[string]` **OR** query parameter: `api_key=[string]`
    * **URL Params**
        * Required:`chain_id=[string]`,`address=[string]`
    * **Example**
      ```shell
      curl --location --request GET 'http://0.0.0.0:5000/api/semantics/dsad/asd' \
      --header 'x-api-key: 05a2212d-9985-48d2-b54f-0fbc5ba28766'
      ```

# New Semantics & Extensions

:point_right: ![Development](DEVELOPMENT.md)
