# Finn.no Job Listings Web Scraper

## Overview
This Python script scrapes today's job listings from the popular Norwegian job board Finn.no, specifically targeting positions in the Oslo area. It extracts select data, stores it in a PostgreSQL database for further analysis and visualization in Power Bi.

## Features
- Scrapes job listings from Finn.no for the Oslo area.
- Retrieves data such as job title, company, sector, and job description.
- Apache Airflow and postgreSQL database in Docker containers for orchestration of pipeline and data storage.
- Provides a "yesterday's stats" dashboard in Power Bi.

## Future work
- Error handling.
- Refactoring.
- Adding more pages to dashboard for further analysis.


The aim of this project is to build a working end-to-end data pipeline while getting more experience with selected tools. Using a job-board as data source whilst looking for work seemed a fun and educational choice.
