<h1 align='center' style="border-bottom: none">
  EthTx Community Edition
</h1>
<br/>
<p align="center">
    <em>Community version of EthTx transaction decoder</em>
<br>
    <em><a href="https://ethtx.info">https://ethtx.info</a></em>
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

# Description

This project represents usage of [EthTx](https://github.com/ethtx/ethtx) decoding library in form of a website. If you
are looking for implementation of the said decoding functionalities, please refer
to [EthTx](https://github.com/ethtx/ethtx) repository.

# Local environment

Here is a list of steps to recreate local environment on <b>Ubuntu</b> distribution.

1. Install needed packages using `apt`:

    ```shell
    apt install docker-compose python3-pip pipenv make
    ```
2. Run:

    ```shell
    pipenv install
    ```

3. Copy `.env_sample` to `.env` and fill required field according to description

    ```
      # Proper nodes are required to run ethtx, provide connection strings for chains which will be used.
      MAINNET_NODE_URL=https://geth-erigon-node:8545
      # KOVAN_NODE_URL=
      # RINKEBY_NODE_URL=

      # EthTx supports multiple nodes, if one is unavailable, it will use others. You only need to specify them with a comma
      # Example: MAINNET_NODE_URL=https://geth-erigon-node:8545,https://geth1-erigon-node:8545


      # Etherscan API is used to get contract source code, required for decoding process
      # You can get free key here https://etherscan.io/apis
      ETHERSCAN_KEY=

      # Optional. Those represent data required for connecting to mongoDB. It's used for caching semantics
      # used in decoding process. But, it's not neccessary for running, If you don't want to use permanent
      # db or setup mongo, leave those values, mongomock package is used to simulate in-memory mongo.
      MONGO_CONNECTION_STRING=mongomock://localhost/ethtx

      # Optional. Credentials for accessing semantics editor page, available under '/semantics/<str:address>'
      ETHTX_ADMIN_USERNAME=admin
      ETHTX_ADMIN_PASSWORD=admin

      # Optional. Api key used for exposing
      API_KEY=

      # Optional. Valid values are ['production', 'staging', 'development']. Those mainly
      # dictate what options are used for flask debugging and logging
      ENV=development
    ```

4. Run
    ```shell
    PYTHONPATH=./ethtx_ce FLASK_APP=ethtx_ce/app/wsgi.py pipenv run flask run --host=0.0.0.0 --port 5000
    ```
   or
    ```shell
    make run-local
    ```
   This will setup new server on host 0.0.0.0 port 5000.
5. Now `ethtx_ce` should be accessible through link [http://localhost:5000](http://localhost:5000)

Use can also provided `docker-compose` for running this locally:

```shell
docker-compose up
```

Note, this also need proper `.env` file to function properly.

# .env file

For proper functioning, `.env` file is required containing all database and 3rd party providers configuration.
`.env_sample` file is provided in repository with example values.

Parameters `[CHAIN_ID]_NODE_URL` should hold valid urls to ethereum nodes; Parameter `ETHERSCAN_KEY` should be equal to
Etherscan API key assigned to user.

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

* **Info**

  Returns information about the `EthTx`

    * **URL**
      ```shell
      /api/info
      ```
    * **Method**
      `GET`
    * **Authorization**
      * Required:
        header: `x-api-key=[string]` **OR** query parameter: `api_key=[string]`
    * **URL Params**
        * None
    * **Example**
      ```shell
      curl --location --request GET 'http://api/info' \
      --header 'x-api-key: 05a2212d-9985-48d2-b54f-0fbc5ba28766'
      ```