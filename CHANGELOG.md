# Changelog

## 1.0.0 (2024-01-30)


### ✨ Feature ✨

* add insecure option to state and module ([08b9993](https://github.com/genaumann/salt-acme.sh-formula/commit/08b9993801d26b66683ae8d5ced1e3b8bcd3e3a9))
* add state files ([c454c40](https://github.com/genaumann/salt-acme.sh-formula/commit/c454c40d6a2792e316f971cbd3de7d230b40e3d6))
* **module:** add acme_sh.cert ([b54956a](https://github.com/genaumann/salt-acme.sh-formula/commit/b54956ad27ee7c92513494b044e9733b59aa155b))
* **module:** add acme_sh.info ([aba0704](https://github.com/genaumann/salt-acme.sh-formula/commit/aba0704f59d6b569ac1e3f55258c99ef716e83a8))
* **module:** add acme_sh.install ([6a72799](https://github.com/genaumann/salt-acme.sh-formula/commit/6a727994cb7461f0ffa055555510cfceebdcef16))
* **module:** add acme_sh.list ([f4c5cee](https://github.com/genaumann/salt-acme.sh-formula/commit/f4c5cee8900d429271e87e0edf75ca6097d83852))
* **module:** add acme_sh.register ([a111c60](https://github.com/genaumann/salt-acme.sh-formula/commit/a111c6050bf48d5360421671f729ece06a7dd862))
* **module:** add acme_sh.renew ([7b79eb1](https://github.com/genaumann/salt-acme.sh-formula/commit/7b79eb1b9e3b68178e2106bbcb27f2ffee9d7510))
* **module:** add acme_sh.version ([c999c36](https://github.com/genaumann/salt-acme.sh-formula/commit/c999c366a188f31f862a3d508fc307251d6ec579))
* **module:** add register info in acme_sh.cert ([c46206d](https://github.com/genaumann/salt-acme.sh-formula/commit/c46206d4585759ba5f33494e0fac3728ef775775))
* **module:** add upgrade and force reinstallation ([e0b63f6](https://github.com/genaumann/salt-acme.sh-formula/commit/e0b63f6c451bb951390cbb2b51b07a586cd79aac))
* **module:** add validTo and validFrom to acme_sh.issue ([f3130b8](https://github.com/genaumann/salt-acme.sh-formula/commit/f3130b802226044a0d8fe33589132f2c951cb2c8))
* **state:** add acme_sh.cert ([208dcf2](https://github.com/genaumann/salt-acme.sh-formula/commit/208dcf236feb6e355ac418ef4ae814b7fdf5181e))
* **state:** add acme_sh.installed ([7b501ec](https://github.com/genaumann/salt-acme.sh-formula/commit/7b501ecebad4834aa4c4884591d991c0b3c3f054))


### 🐛 Bugfix 🐛

* if condition in map.jinja ([9fe89e1](https://github.com/genaumann/salt-acme.sh-formula/commit/9fe89e120f9da1e302325709b48d53b0190355f7))
* **module:** add better error checking for state ([d930904](https://github.com/genaumann/salt-acme.sh-formula/commit/d9309044bd230b3bd1a603c162346ffd0b4884be))
* **module:** cert-path to cert-home ([5bb2331](https://github.com/genaumann/salt-acme.sh-formula/commit/5bb2331e2525f08e2a095e52fe43e4d769b42a7a))
* **state:** handle strings ([5dc27ee](https://github.com/genaumann/salt-acme.sh-formula/commit/5dc27ee4fca085c1633c3c88fb133a820e354579))


### 💿 Continuous Integration 💿

* change opensuse salt version ([a45fcee](https://github.com/genaumann/salt-acme.sh-formula/commit/a45fcee9329e239645d79e43343efd82d8360210))
* **github:** add CRED var before kitchen test ([3a6f9cd](https://github.com/genaumann/salt-acme.sh-formula/commit/3a6f9cd855f4017d6fa1e50c815c5588a0bcf230))
* **github:** run release on successfull test [skip ci] ([b197d18](https://github.com/genaumann/salt-acme.sh-formula/commit/b197d18ef4df7ee0103beeeb0b7f1a408c845b75))
* **github:** set ruby version to 3.2.2 ([58a89ad](https://github.com/genaumann/salt-acme.sh-formula/commit/58a89ad312aeeaf39fc5cd5827cd13af991e1a5b))
* **release:** don't trigger release on ci type ([26d45dc](https://github.com/genaumann/salt-acme.sh-formula/commit/26d45dcebc1704b2d442ab121a5e2ab527d89a74))


### 🖌️ Style 🖌️

* add pylint suggestions ([9a2ed23](https://github.com/genaumann/salt-acme.sh-formula/commit/9a2ed23f5344706237d132f21f6dcb950c92c33f))
* apply rubocop recommendations ([c1f605d](https://github.com/genaumann/salt-acme.sh-formula/commit/c1f605d428edc4cf64b87142d5366a216ddb259c))
* fix ide warnings ([1aafc9a](https://github.com/genaumann/salt-acme.sh-formula/commit/1aafc9a56261f8fe8aaaebbcb9626d576d5b6d63))


### 🧪 Test 🧪

* add more domains to test cases ([c471522](https://github.com/genaumann/salt-acme.sh-formula/commit/c471522005143fe123b9b63851d1ce45496178d6))
* add salt pre test scripts and pillar ([49a0d5f](https://github.com/genaumann/salt-acme.sh-formula/commit/49a0d5f95ae1e677f98b1f008f702db8e92c11c7))
* add test cases ([64dc334](https://github.com/genaumann/salt-acme.sh-formula/commit/64dc334426b49f3a8b1593feeb9d64f654977297))
* fix nxdomain error ([3eb0b59](https://github.com/genaumann/salt-acme.sh-formula/commit/3eb0b591bfa7728b571df330defc63e2f843fd3c))


### 📖 Documentation 📖

* add example pillar file ([3778f49](https://github.com/genaumann/salt-acme.sh-formula/commit/3778f49009cd30d90b4c113234335ff7582aaf08))
* add state and module docs ([8289316](https://github.com/genaumann/salt-acme.sh-formula/commit/828931655cc9626cad2c7dc25cbf068eb3137547))
