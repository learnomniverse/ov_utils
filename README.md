Please read [https://learnomniverse.github.io/](https://learnomniverse.github.io/) for more information.

Use this repo as a git submodule in your main Omniverse extension development repository to download and configure Omniverse dependencies via Conan recipes and set up a local filesystem building hierarchy via CMake helpers.

Here's a quick git cheatsheet
```bash
# Add this ov_utils repo as a git submodule of your main ov extension repo
your_ov_repo$ git submodule add git@github.com:learnomniverse/ov_utils.git ov_utils
your_ov_repo$ git commit -m "Added ov_utils submodule"
# Clone your main ov extension repo along with the ov_utils submodule
your_ov_repo$ git clone --recursive <your_ov_repo_url>
# or do it later if you already checked it out
your_ov_repo$ git submodule update --init --recursive
# update the submodule to latest version
your_ov_repo$ cd ov_utils # go to the path of the submodule that you specified
your_ov_repo$ git pull origin master
your_ov_repo$ cd .. # go back to main ov repo root
your_ov_repo$ git add ov_utils # add changes to the submodule
your_ov_repo$ git commit -m "Update ov_utils to the latest commit"
```
