<a id="readme-top"></a>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">FontAwesome 6 LaTeX Package & Builder</h3>

  <p align="center">
    <a href="https://github.com/D-Naveenz/fontawsome6-latex/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/D-Naveenz/fontawsome6-latex/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#prerequisites">Prerequisites</a>
    </li>
    <li><a href="#usage">Usage</a>
      <ul>
        <li><a href="#use-the-built-package">Use the built package</a></li>
        <li><a href="#make-latest-fontawesome6-package">Make Latest fontawesome6 package</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is a build script for generating a LaTeX package for FontAwesome 6 icons. FontAwesome is a popular icon set and toolkit, and this script facilitates its integration into LaTeX documents by creating a custom .sty file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Features
* **Automated Build Process:** The script downloads and processes FontAwesome 6 icons metadata to generate a LaTeX package.
* **Customizable Output:** The resulting package includes a .sty file with all necessary icon definitions, ready to be included in LaTeX documents.
* **Easy Integration:** The package can be easily integrated into LaTeX projects, allowing the use of FontAwesome 6 icons in your documents.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![LaTeX][latex-shield]][latex-url] [![python][python-shield]][python-url]



## Prerequisites

* You must have the FontAwesome font on your machine (download from [here](https://fontawesome.com/)).
* You must be using XeLaTeX and have the `fontspec` package installed.
* You can use this package with the free and the pro fonts.
* For using the pro features, you need to buy [Font Awesome Pro](https://fontawesome.com/pro).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Use the built package

1. Download the `fontawesome.zip` file from releases if you don't have and put it in the same directory as the LaTeX file using the icons.
2. Extact it into the `fontawesome` folder.
3. Include the package as normal (in the preamble of the `.tex` file, add the line `\usepackage{fontawesome/fontawesome6}`).
4. Use an icon by typing `\faIcon{address-book}`. Other icons than `address-book` can be found on the [fontawesome](https://fontawesome.com/icons?d=gallery) website.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Example

##### Free version
```tex
\usepackage{fontawesome/fontawesome6}

\faIcon{font-awesome}
Normal: \faIcon{address-book}
Bold: \textbf{\faIcon{address-book}}
```

```bash
$ xelatex example-free.tex
```

##### Pro version
```tex
\usepackage[pro]{fontawesome/fontawesome6}

\faIcon{font-awesome}
Normal: \faIcon{alarm-clock}
Bold: \textbf{\faIcon{alarm-clock}}
Italic: \textit{\faIcon{alarm-clock}}
```

```bash
$ xelatex example-pro.tex
```

### Make Latest fontawesome6 package

#### Requirements
* You need python to create `fontawesome6.sty` from scratch.
* Download FontAwesome from [here](https://fontawesome.com/download) and exctact the zip file into `fontawesome` folder

#### Usage
```bash
$ python build.py
```
This should result in the creation of **latest** ``fontawesome6.sty``

---



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Naveen Dharmathunga - [@XerDuke](https://x.com/dharmathunga) - dasheenaveen@outlook.com

Project Link: <https://github.com/D-Naveenz/fontawsome6-latex>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Latex Team](https://www.latex-project.org/about/team/)
* [Python](https://www.python.org/about/)
* [Img Shields](https://shields.io)
* [Font Awesome](https://fontawesome.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/D-Naveenz/NextCV.svg?style=for-the-badge
[contributors-url]: https://github.com/D-Naveenz/fontawsome6-latex/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/D-Naveenz/NextCV.svg?style=for-the-badge
[forks-url]: https://github.com/D-Naveenz/fontawsome6-latex/network/members
[stars-shield]: https://img.shields.io/github/stars/D-Naveenz/NextCV.svg?style=for-the-badge
[stars-url]: https://github.com/D-Naveenz/fontawsome6-latex/stargazers
[issues-shield]: https://img.shields.io/github/issues/D-Naveenz/NextCV.svg?style=for-the-badge
[issues-url]: https://github.com/D-Naveenz/fontawsome6-latex/issues
[license-shield]: https://img.shields.io/github/license/D-Naveenz/NextCV.svg?style=for-the-badge
[license-url]: https://github.com/D-Naveenz/fontawsome6-latex/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/dasheewd/
[latex-shield]: https://img.shields.io/badge/latex-%23008080.svg?style=for-the-badge&logo=latex&logoColor=white
[Latex-url]: https://www.latex-project.org/
[python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/
