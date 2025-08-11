

(.venv) PS C:\\Users\\nasim\\Documents\\git\\sims> flask db upgrade

INFO  \[alembic.runtime.migration] Context impl SQLiteImpl.

INFO  \[alembic.runtime.migration] Will assume non-transactional DDL.

INFO  \[alembic.runtime.migration] Running upgrade  -> 1f4ea347272c, empty message

Traceback (most recent call last):

&nbsp; File "<frozen runpy>", line 198, in \_run\_module\_as\_main

&nbsp; File "<frozen runpy>", line 88, in \_run\_code

&nbsp; File "C:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Scripts\\flask.exe\\\_\_main\_\_.py", line 7, in <module>

&nbsp;   sys.exit(main())

&nbsp;            ~~~~^^

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\flask\\cli.py", line 1105, in main

&nbsp;   cli.main()

&nbsp;   ~~~~~~~~^^

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\click\\core.py", line 1078, in main

&nbsp;   rv = self.invoke(ctx)

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\click\\core.py", line 1688, in invoke

&nbsp;   return \_process\_result(sub\_ctx.command.invoke(sub\_ctx))

&nbsp;                          ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\click\\core.py", line 1688, in invoke

&nbsp;   return \_process\_result(sub\_ctx.command.invoke(sub\_ctx))

&nbsp;                          ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\click\\core.py", line 1434, in invoke

&nbsp;   return ctx.invoke(self.callback, \*\*ctx.params)

&nbsp;          ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\click\\core.py", line 783, in invoke

&nbsp;   return \_\_callback(\*args, \*\*kwargs)

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\click\\decorators.py", line 33, in new\_func

&nbsp;   return f(get\_current\_context(), \*args, \*\*kwargs)

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\flask\\cli.py", line 386, in decorator

&nbsp;   return ctx.invoke(f, \*args, \*\*kwargs)

&nbsp;          ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\click\\core.py", line 783, in invoke

&nbsp;   return \_\_callback(\*args, \*\*kwargs)

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\flask\_migrate\\cli.py", line 157, in upgrade

&nbsp;   \_upgrade(directory or g.directory, revision, sql, tag, x\_arg or g.x\_arg)

&nbsp;   ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\flask\_migrate\\\_\_init\_\_.py", line 111, in wrapped

&nbsp;   f(\*args, \*\*kwargs)

&nbsp;   ~^^^^^^^^^^^^^^^^^

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\flask\_migrate\\\_\_init\_\_.py", line 200, in upgrade

&nbsp;   command.upgrade(config, revision, sql=sql, tag=tag)

&nbsp;   ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\alembic\\command.py", line 483, in upgrade

&nbsp;   script.run\_env()

&nbsp;   ~~~~~~~~~~~~~~^^

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\alembic\\script\\base.py", line 551, in run\_env

&nbsp;   util.load\_python\_file(self.dir, "env.py")

&nbsp;   ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\alembic\\util\\pyfiles.py", line 116, in load\_python\_file

&nbsp;   module = load\_module\_py(module\_id, path)

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\alembic\\util\\pyfiles.py", line 136, in load\_module\_py

&nbsp;   spec.loader.exec\_module(module)  # type: ignore

&nbsp;   ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^

&nbsp; File "<frozen importlib.\_bootstrap\_external>", line 1026, in exec\_module

&nbsp; File "<frozen importlib.\_bootstrap>", line 488, in \_call\_with\_frames\_removed

&nbsp; File "C:\\Users\\nasim\\Documents\\git\\sims\\migrations\\env.py", line 113, in <module>

&nbsp;   run\_migrations\_online()

&nbsp;   ~~~~~~~~~~~~~~~~~~~~~^^

&nbsp; File "C:\\Users\\nasim\\Documents\\git\\sims\\migrations\\env.py", line 107, in run\_migrations\_online

&nbsp;   context.run\_migrations()

&nbsp;   ~~~~~~~~~~~~~~~~~~~~~~^^

&nbsp; File "<string>", line 8, in run\_migrations

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\alembic\\runtime\\environment.py", line 946, in run\_migrations

&nbsp;   self.get\_context().run\_migrations(\*\*kw)

&nbsp;   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^

&nbsp; File "c:\\Users\\nasim\\Documents\\git\\sims\\.venv\\Lib\\site-packages\\alembic\\runtime\\migration.py", line 627, in run\_migrations

&nbsp;   step.migration\_fn(\*\*kw)

&nbsp;   ~~~~~~~~~~~~~~~~~^^^^^^

&nbsp; File "C:\\Users\\nasim\\Documents\\git\\sims\\migrations\\versions\\1f4ea347272c\_.py", line 26, in upgrade

&nbsp;   sa.Column('email', sqlalchemy\_utils.types.email.EmailType(length=255), nullable=True),

&nbsp;                      ^^^^^^^^^^^^^^^^

NameError: name 'sqlalchemy\_utils' is not defined















