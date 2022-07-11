# Changelog
All notable changes to this project will be documented in this file.

## 0.2.15 - 2022-07-06
### Changed
- Removed `Tokne Flow` branding

### Added
- Added redecode semantics functionality
- Bumped `EthTx` to `0.3.16` [#116](https://github.com/EthTx/ethtx_ce/pull/116)
- From now on the value of `transfer.value` is formatted on the frontend [#116](https://github.com/EthTx/ethtx_ce/pull/116)

### Fixed
- Fixed wrong function name (`get_semantics`) [#118](https://github.com/EthTx/ethtx_ce/pull/118)


## 0.2.14 - 2022-05-18
### Added
- Added `info` endpoint with ethtx/ethtx_ce version [#113](https://github.com/EthTx/ethtx_ce/pull/113)
- added `get_latest_ethtx_version` function (get version from Pypi) [#113](https://github.com/EthTx/ethtx_ce/pull/113)

### Changed
- Refactored `deps` [#113](https://github.com/EthTx/ethtx_ce/pull/113)
- Updated `README.md` [#113](https://github.com/EthTx/ethtx_ce/pull/113)
- Updated `black` version [#113](https://github.com/EthTx/ethtx_ce/pull/113)
- Changed the application name for each component [#113](https://github.com/EthTx/ethtx_ce/pull/113)


## 0.2.13 - 2022-04-22
### Changed
- Extended *.gitignore* [#110](https://github.com/EthTx/ethtx_ce/pull/110)
- Updated `black` pre-commit version [#110](https://github.com/EthTx/ethtx_ce/pull/110)

### Fixed
- Fixed mongodb semantics remove [#110](https://github.com/EthTx/ethtx_ce/pull/110)


## 0.2.12 - 2022-04-06
### Changed
- Bumped `EthTx` to `0.3.14` [#105](https://github.com/EthTx/ethtx_ce/pull/105)


## 0.2.11 - 2022-03-16
### Changed
- New project structure [#97](https://github.com/EthTx/ethtx_ce/pull/97)
- Updated docker, docker-compose [#97](https://github.com/EthTx/ethtx_ce/pull/97)
- Removed logs, useless text [#99](https://github.com/EthTx/ethtx_ce/pull/99)
- Changed space between *tx_hash* and *chain_id* (transaction page) [#99](https://github.com/EthTx/ethtx_ce/pull/99)

### Added
- Added gunicorn configuration [#97](https://github.com/EthTx/ethtx_ce/pull/97)
- Added `entrypoint.sh` and other scripts [#97](https://github.com/EthTx/ethtx_ce/pull/97)


## 0.2.10 - 2022-03-03
### Changed
- Bumped `EthTx` to `0.3.10` [#93](https://github.com/EthTx/ethtx_ce/pull/93)


## 0.2.9 - 2022-02-07
### Fixed
- Typo in `README.md` [#75](https://github.com/EthTx/ethtx_ce/pull/75)
- API serialization [#75](https://github.com/EthTx/ethtx_ce/pull/75)
- Fixed semantics editor [#75](https://github.com/EthTx/ethtx_ce/pull/75)
- Fixed `.env_sample` mongo connection string [#83](https://github.com/EthTx/ethtx_ce/pull/83)

### Added
- Added new route `reload`
- Added `Reolad semantics` button, which allows to reload the semantics (removes from the database and downloads
  again) [#80](https://github.com/EthTx/ethtx_ce/pull/80)
- Added `get_eth_price`. Transaction page displays current **ETH** price taken from *coinbase*
  API [#88](https://github.com/EthTx/ethtx_ce/pull/88)

### Changed
- Removed duplicated environment variables from `docker-compose.yml` [#83](https://github.com/EthTx/ethtx_ce/pull/83)
- Bumped python to `3.9` [#87](https://github.com/EthTx/ethtx_ce/pull/87)
- From now on, `EthTx` will be used with a static version (due to dynamic
  development) [#87](https://github.com/EthTx/ethtx_ce/pull/87)
- Updated requirements [#88](https://github.com/EthTx/ethtx_ce/pull/88)
- Install dev dependencies [#89](https://github.com/EthTx/ethtx_ce/pull/89)


## 0.2.8 - 2021-10-29
### Changed
- Updated **README** and **.env_sample** [#67](https://github.com/EthTx/ethtx_ce/pull/67)
- `Web3ConnectionException` is not supported anymore. From now on, a general exception `NodeConnectionException`
  is caught for node connection errors  [#67](https://github.com/EthTx/ethtx_ce/pull/67)
- Guessed functions and events are detected using the guessed variable in the
  model [#67](https://github.com/EthTx/ethtx_ce/pull/67)


## 0.2.7 - 2021-10-14
### Changed
- Changed [EthTx](https://github.com/EthTx/ethtx) version - >=0.3.0,<
  0.4.0 [#62](https://github.com/EthTx/ethtx_ce/pull/62)
- Deleted usage of mongodb variable [#61](https://github.com/EthTx/ethtx_ce/pull/61)

### Fixed
- Fixed colored guessed events with tuple arg [#65](https://github.com/EthTx/ethtx_ce/pull/65)


## 0.2.6 - 2021-10-01
### Changed
- Changed the position of the logo [#59](https://github.com/EthTx/ethtx_ce/pull/59)


## 0.2.5 - 2021-09-30
### Fixed
- Fixed colored guessed functions with nested args [#58](https://github.com/EthTx/ethtx_ce/pull/58)


## 0.2.4 - 2021-09-29
### Added
- Added `.env_sample` file with example environment variables [#57](https://github.com/EthTx/ethtx_ce/pull/57)

### Fixed
- Fixed `make run-local` [#57](https://github.com/EthTx/ethtx_ce/pull/57)

### Changed
- Changed the docker configuration to make it easier to start [#57](https://github.com/EthTx/ethtx_ce/pull/57)
- Updated **README** [#57](https://github.com/EthTx/ethtx_ce/pull/57)


## 0.2.3 - 2021-09-23
### Added
- Color guessed functions and events [#56](https://github.com/EthTx/ethtx_ce/pull/56)


## 0.2.2 - 2021-09-20
### Fixed
- Fixed `tx hash` regexp extracting from request [#53](https://github.com/EthTx/ethtx_ce/pull/53)


## 0.2.1 - 2021-09-17
### Fixed
- Fixed `Decode now` button state [#50](https://github.com/EthTx/ethtx_ce/pull/50)


## 0.2.0 - 2021-09-14
### Added - [#44](https://github.com/EthTx/ethtx_ce/pull/44)
- Added new error page.
- Added [Token Flow](https://tokenflow.live) logo.
- Added input hash validator.

### Changed - [#44](https://github.com/EthTx/ethtx_ce/pull/44)
- Changed footer style.
- Removed **ToS** and **PP** and replaced them with `Token Flow` pages.
- Removed old tests.
- Added **Fathom** analytics tool.
- Updated links.

### Fixed - [#44](https://github.com/EthTx/ethtx_ce/pull/44)
- Fixed frontend styles.


## 0.1.10 - 2021-08-20
### Added
- Added *preload* to links.


## 0.1.9 - 2021-08-18
### Added
- Added new footer.
- Added `Rinkeby` support.

### Changed
- Changed [EthTx](https://github.com/EthTx/ethtx) version - >=0.2.0,<0.3.0.

### Fixed
- Etherscan links fixed for testnets.


## 0.1.8 - 2021-08-11
### Added
- Added `Goerli` support.

### Changed
- Changed [EthTx](https://github.com/EthTx/ethtx) version - >=0.2.0,<0.3.0.

## 0.1.7 - 2021-08-05
### Added
- Added link to PyPi.


## 0.1.6 - 2021-08-04
### Added
- Added information about the `EthTx` and `EthTx Ce` version to the frontend.

### Changed
- Removed `Pipfile.lock`

### Fixed
- Fixed application dependencies.


## 0.1.5 - 2021-08-02
### Changed
- Removed the banner that was about the new version of `ethtx_ce`.


## 0.1.4 - 2021-07-29
### Changed
- Changed semantics save functions.
- Changed [EthTx](https://github.com/EthTx/ethtx) version - 0.1.7.


## 0.1.3 - 2021-07-28
### Changed
- Changed [EthTx](https://github.com/EthTx/ethtx) version - 0.1.6.


## 0.1.2 - 2021-07-27
### Changed
- Changed [EthTx](https://github.com/EthTx/ethtx) version - 0.1.5.
- Changed app Config.
- Removed EthtxConfig defaults.


## 0.1.1 - 2021-07-26
### Fixed
- Fixed header on mobile devices.

### Changed
- Changed Development.MD note.

### Added
- Added configuration: AWS, Pipfile, pre-commit.

## 0.1.0 - 2021-07-23
### Added
- First version EthTx CE.
