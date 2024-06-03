<h3 align="center">{{cookiecutter.project_name}}</h3>

<div align="center">
  <p>{{ cookiecutter.project_short_description }}</p>
</div>

<div align="center">

  [![GitHub Issues][github-issues-shield]][github-issues-url]
  [![GitHub Pull Requests][github-prs-shield]][github-prs-url]
  [![License][license-shield]][license-url]

</div>

<div align="center">
  <p><a href="http://{{ cookiecutter.project_url.split('/')[-2] }}.github.io/{{ cookiecutter.project_url.split('/')[-1] }}/latest"><strong>Explore the latest docs »</strong></a></p>
</div>

---

<!-- FEATURES -->
## ✨ Features

<!-- GETTING STARTED -->
## 🚀 Getting Started

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
```sh
npm install npm@latest -g
```
### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
```sh
git clone https://github.com/your_username_/Project-Name.git
```
3. Install NPM packages
```sh
npm install
```
4. Enter your API in `config.js`
```JS
const API_KEY = 'ENTER YOUR API';
```

<!-- USAGE EXAMPLES -->
## 🛠️ Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<!-- ROADMAP -->
## 🚧 Roadmap

See the [open issues]({{ cookiecutter.project_url }}/issues) for a list of proposed features (and known issues).

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

Distributed under the {{ cookiecutter.project_license }} License. See [`LICENSE`]({{ cookiecutter.project_url }}/blog/main/LICENSE) for more information.

<!-- CONTACT -->
## 📫 Contact

{{ cookiecutter.author_name }} - {{ cookiecutter.author_email }}

Project Link: [{{ cookiecutter.project_url }}]({{ cookiecutter.project_url }})

<!-- ACKNOWLEDGEMENTS -->
## 🙏 Acknowledgements

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[github-issues-shield]: https://img.shields.io/github/issues/{{ cookiecutter.project_url.split('/')[-2] }}/{{ cookiecutter.project_url.split('/')[-1] }}
[github-issues-url]: https://github.com/{{ cookiecutter.project_url.split('/')[-2] }}/{{ cookiecutter.project_url.split('/')[-1] }}/issues
[github-prs-shield]: https://img.shields.io/github/issues-pr/{{ cookiecutter.project_url.split('/')[-2] }}/{{ cookiecutter.project_url.split('/')[-1] }}
[github-prs-url]: https://github.com/{{ cookiecutter.project_url.split('/')[-2] }}/{{ cookiecutter.project_url.split('/')[-1] }}/pulls
[license-shield]: https://img.shields.io/github/license/{{ cookiecutter.project_url.split('/')[-2] }}/{{ cookiecutter.project_url.split('/')[-1] }}
[license-url]: {{ cookiecutter.project_url }}/blob/main/LICENSE
