# Human in the Loop (Hil)

Add description **[TODO]**

## Dependencies

- Python 3.5

## Getting Started

1. Create a new main file:

  ```console
  $ touch app.py
  ```

   where `app` is the main application.

2. Open the `app.py` file and import hil core:

  ```python
  from hil import Core
  ```

3. Create a new component file:

  ```console
  $ touch bell.py
  ```

   where `bell` is a sub application.

3. Open the `bell.py` file and write a sample component:

  ```python
  from hil import Component

  class Bell(Component):
    def play():
      print(chr(7))
      return None
  ```

4. Open the `app.py`and import the new component into your main application:

  ```python
  from bell import Bell
  ```

5. Initialize the core framework:

  ```python
  core = Core()
  ```

6. Add the new component class:

  ```python
  core.addComponent(Bell)
  ```

7. Add the run command to your main server:

  ```python
  core.start()
  ```

8. Run your server:

  ```console
  $ python3 app.py
  ```

9. Open a terninal and run the following command:

  ```console
  $ curl -X POST --data "component=Bell&event=play" http://localhost:8000
  ```

## Api Documentation

Using a browser, go to `http://localhost:8000/documentation` and you'll see the documentation of the api.


## Sample Apps

There is a sample app at <https://github.com/fvioz/hil-sample> please check
