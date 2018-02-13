# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [9.0.1.0.4] - 2018-02-13
### changed
- Fix: Refactoring to method _get_delivery_carrier_id(), accepting available carriers ids as parameter for avoid have to querying by them.

## [9.0.1.0.3] - 2018-02-09
### changed
- Fix: Add parameter website to method that queries for carriers valid to allows search only in those published in website.

## [9.0.1.0.2] - 2018-02-09
### changed
- Refactoring to code separating in method to obtain the carrier, so that this method is reused from other modules.

## [9.0.1.0.1] - 2017-12-09
### changed
- Fix bug in inheritance of method button_dummy in model sale.order.


## [9.0.1.0.0] - 2017-12-09
### added
- Autodetects delivery method in sale orders according to zip code of customer and better price by volume total or weight total.
