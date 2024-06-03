<h3 align="center">{{cookiecutter.project_name}}</h3>

<div align="center">
  <p>{{ cookiecutter.project_short_description }}</p>
</div>

<div align="center">

  [![GitHub Issues][github-issues-shield]][github-issues-url]
  [![GitHub Pull Requests][github-prs-shield]][github-prs-url]
  [![License][project-license-shield]][project-license-url]

</div>

<div align="center">

[**Explore the latest docs »**][project-docs-url]

</div>

---

Detailed description about {{ cookiecutter.project_name }} goes here.

---

<!-- FEATURES -->
## ✨ Features

<!-- GETTING STARTED -->
## 🚀 Getting Started

### Prerequisites

* [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### Installation

1. Clone the repo
```sh
git clone {{ cookiecutter.project_url }}.git
```
2. Install
```sh
poetry install
```

<!-- USAGE EXAMPLES -->
## 🛠️ Usage

Show a few examples of how a project is to be used.

_For more examples, please refer to the [documentation][project-docs-url]_

<!-- ROADMAP -->
## 🚧 Roadmap

See the [open issues][github-issues-url] for a list of proposed features (and known issues).

<!-- TODO -->
## ☑️ TODO
- [ ] TODO 1

<!-- CONTRIBUTING -->
## 🤝 Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **extremely appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## 📝 License

Distributed under the {{ cookiecutter.project_license }} License. See [`LICENSE`][project-license-url] for more information.

<!-- CONTACT -->
## 📫 Contact

{{ cookiecutter.author_name }} - {{ cookiecutter.author_email }}

Project Link: [{{ cookiecutter.project_url }}][project-url]

<!-- ACKNOWLEDGEMENTS -->
## 🙏 Acknowledgements

Anyone you'd like to thank?

<!-- MARKDOWN REFERENCE LINKS -->
[project-url]: {{ cookiecutter.project_url }}
[project-docs-url]: https://{{ cookiecutter.project_url.split('/')[-2] }}.github.io/{{ cookiecutter.project_url.split('/')[-1] }}/latest
[project-license-shield]: https://img.shields.io/github/license/{{ cookiecutter.project_url.split('/')[-2] }}/{{ cookiecutter.project_url.split('/')[-1] }}
[project-license-url]: {{ cookiecutter.project_url }}/blob/main/LICENSE
[github-issues-shield]: https://img.shields.io/github/issues/{{ cookiecutter.project_url.split('/')[-2] }}/{{ cookiecutter.project_url.split('/')[-1] }}
[github-issues-url]: https://github.com/{{ cookiecutter.project_url.split('/')[-2] }}/{{ cookiecutter.project_url.split('/')[-1] }}/issues
[github-prs-shield]: https://img.shields.io/github/issues-pr/{{ cookiecutter.project_url.split('/')[-2] }}/{{ cookiecutter.project_url.split('/')[-1] }}
[github-prs-url]: https://github.com/{{ cookiecutter.project_url.split('/')[-2] }}/{{ cookiecutter.project_url.split('/')[-1] }}/pulls
