# MarketPlace

Sell your goods on our market (API)

![PyPI pyversions](https://img.shields.io/badge/python-3.11-blue)
![License: MIT](https://img.shields.io/github/license/eli64s/readme-ai?color=blueviolet)

---

## 🔗 Quick Links
* [Overview](#-overview)
* [Getting Started](#-getting-started)
* [License](#-license)

---

## 🔭 Overview
***Stack***

FastApi, ElasticSearch, Docker

***Products***

The product can be added with any additional parameters. 
Storage and receipt of goods is carried out using elasticsearch.

> [!NOTE]
This project is just a microservice 
> for storing products, in order to implement
> a full marketplace, you also need a user base
>
---
## 👩‍💻 Getting Started

***Dependencies***

Please ensure you have the following dependencies installed on your system:

- *Python version 3.11 or higher*
- *Package manager poetry or Docker*


***MarketPlace API***

An  .env file is needed to use *Manager Passwords API*
The steps below outline this process to create it:

<details closed><summary>🔐 MarketPlace API - .env file</summary>
You need to create variables to connect to the database in the .env file

For example:

- *ES_PORT: 9200*
- *ES_DATABASE: es*

</details>
---
### 🚀 Running *MarketPlace*

Using `docker`

```bash
docker compose -f docker-compose-dev.yaml up -d
```

### 📝 Documentation

API documentation will be available after running
[Documentation](http://localhost:8000/docs) at http://localhost:8000/docs

---

### 🧪 Tests

Execute the test suite using the command below.

```bash
 docker compose -f docker-compose-test.yaml up -d
```

---

## 📄 License

[MIT](https://github.com/eli64s/readme-ai/blob/main/LICENSE)

---
