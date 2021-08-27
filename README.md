<h1 align='center' style="border-bottom: none">
  EthTx Community Edition
</h1>
<h3 align='center' style="border-bottom: none">
  Supports BSC and Polygon
</h3>
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
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="Apache">
</a>
</p>

---

# Local environment

For local instance, you need few things:

0. Depending on your distribution, install: docker, docker-compose, python3-pip, pipenv
1. mongoDB - to set it up for the first time, execute this command: `make run-database`
2. pipenv - to create virtual env run command `pipenv install`, this should create venv for this project with all python
   dependencies.

After this, if you want to run any command inside this env, use `pipenv run` or `pipenv shell`.

To run flask server localy, use `make run-local` command, this will setup new server on host 0.0.0.0 port 5000

# .env file

For proper functioning, `.env` file is required containing all database and 3rd party providers configuration.
`.env` file is provided in repository with default values and should be good to use if nothing else was changed.

Parameters `[CHAIN_ID]_NODE_URL` should hold valid urls to ethereum nodes; Parameter `ETHERSCAN_KEY` should be equal to
Etherscan API key assigned to user.

Fill in the values in the `.env` file and leave `ETHERSCAN_KEY`/`MAINNET_NODE_URL`/`GOERLI_NODE_URL`/`RINKEBY_NODE_URL` empty if you do not need to support the ethereum main and test networks.

`BSC_NODE_URL` and `POLYGON_NODE_URL` value fill in the `apikey url` of the `getblock.io` , example: `https://bsc.getblock.io/mainnet/?api_key=xxx`

# .docker_env file
The content of file `.docker_env` is the same as that of file `.env`, but file `.docker_env` is used for docker container, so the `MONGO_CONNECTION_STRING` value may need to be modified, and can not be connected to `127.0.0.1`, but to the internal IP of MongoDB

# wsgi.py file
Modify the key/value pairs in the `etherscan_urls` dict, apply the `APIKey` in `bscscan.com` and `Polygonscan.com` respectively, then concatenate the `APIKey` into the `API URL`, then fill the full URL into the `BSC key` and `Polygon key`

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
