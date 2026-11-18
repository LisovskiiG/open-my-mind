# OpenMyMind 2.0

[English](#english) · [Русский](#русский) · [Қазақша](#қазақша)

## English

OpenMyMind is a ChatGPT plugin that gives you time to form your own answer before seeing the model's explanation. Use it to understand a new concept, test an assumption, or practise explaining your reasoning.

<img width="1672" height="941" alt="Think_yourself_first" src="https://github.com/user-attachments/assets/510e49a5-1b55-47ab-b364-461bfbe381a9" />

### Start an exercise

1. Install OpenMyMind in ChatGPT and open a new chat.
2. Select `@OpenMyMind` and ask a question. You can name a mode in the same message or choose one when prompted.
3. Share your reasoning, choose a quiz option, or ask for the direct answer whenever you need it.

| Mode | What happens | Example prompt |
| --- | --- | --- |
| **Guiding questions** | The plugin asks 3–5 open-ended questions and waits. Answering one is enough to start a review of your reasoning, get a direct answer and see how to check the main conclusion. You can also ask for a hint. | “Use guiding questions to help me work out why Git uses branches.” |
| **Quiz** | Choose from three options. If you pick the correct one, the plugin explains the reasoning in more depth. If you pick another option, it explains where that reasoning goes wrong and walks through the correct one. | “Give me a short reasoning quiz.” |
| **Propose a hypothesis** | Give your own answer first. If you are close, the plugin explains what you got right and fills in the gaps. Otherwise, it points out a gap and offers another attempt, another mode, or the direct answer. | “Let me propose a hypothesis about why ice floats.” |

### Track your progress

Connect your OpenMyMind account and explicitly turn on progress tracking. Then ask for a report over the last **7 days**, **30 days**, or **all time**. The report counts completed exercises by outcome, including independent answers, answers after guiding questions, and direct answers requested before practice. It also lists quiz results and direct answers requested after starting an exercise.

The chart shows the share of completed exercises answered independently, with quiz results counted separately. The 7- and 30-day reports group results by day in UTC. The all-time report groups them by month. This percentage describes your activity in OpenMyMind. The server stores outcome categories and timestamps. The text of your questions and answers stays outside its database. Turning off tracking stops future recording and keeps your existing results.

Try **“Show my OpenMyMind progress for the last 7 days.”**

### Set email reminders

Connect an account with a verified email address. Ask OpenMyMind to remind you **daily** or **every three days**. The first reminder is scheduled after the selected interval. To change the frequency, ask in chat. To stop reminders, ask in chat or use the link in an email.

Try **“Remind me to practise every three days.”**

### Setup and language

The training modes can run as a skill-based plugin in ChatGPT. Progress tracking and OpenMyMind's own email reminders require a connected MCP backend. The current build runs the Python MCP server and email worker as separate processes. See the [deployment guide](#развёртывание-сервера) below. The plugin replies in your language. Charts and reminder emails currently use English.

## Русский

OpenMyMind — плагин для ChatGPT, который даёт время сформулировать свой ответ перед тем, как прочитать объяснение модели. Используйте его, когда хотите разобраться в новом понятии, проверить предположение или потренироваться объяснять ход своих мыслей.

<img width="1672" height="941" alt="Think_yourself_first" src="https://github.com/user-attachments/assets/510e49a5-1b55-47ab-b364-461bfbe381a9" />

### Начните упражнение

1. Установите OpenMyMind в ChatGPT и откройте новый чат.
2. Выберите `@OpenMyMind` и задайте вопрос. Режим можно указать сразу или выбрать из предложенных.
3. Поделитесь рассуждением, выберите вариант в квизе или попросите готовый ответ в любой момент.

| Режим | Как проходит упражнение | Пример запроса |
| --- | --- | --- |
| **Наводящие вопросы** | Плагин задаёт 3–5 открытых вопросов и ждёт вашей реплики. Достаточно ответить на один, чтобы получить разбор рассуждения, прямой ответ и способ проверить основной вывод. Можно попросить подсказку. | «Помоги разобраться, зачем Git нужны ветки. Задай наводящие вопросы». |
| **Квиз** | Выберите один из трёх вариантов. Если выбор верный, плагин подробнее объяснит ход рассуждения. Если вы ошиблись, он разберёт конкретную ошибку и покажет, как прийти к верному ответу. | «Дай мне короткий квиз на логику». |
| **Предложите свою гипотезу** | Сначала дайте свой ответ. Если он близок по смыслу, плагин отметит, что вы уловили, и дополнит объяснение. Если в рассуждении есть существенный пробел, плагин укажет на него и предложит повторить попытку, сменить режим или получить готовый ответ. | «Хочу предложить свою гипотезу о том, почему лёд плавает». |

### Следите за прогрессом

Подключите аккаунт OpenMyMind и отдельно включите сбор статистики. Затем запросите отчёт за **7 дней**, **30 дней** или **всё время**. В отчёте подсчитываются самостоятельные ответы, ответы после наводящих вопросов и прямые ответы, запрошенные до начала упражнения. Отдельно учитываются результаты квиза и случаи, когда готовый ответ запросили уже после начала упражнения.

График показывает долю самостоятельных ответов среди завершённых упражнений вне квиза. За 7 и 30 дней результаты группируются по дням в UTC, а за всё время — по месяцам. Показатель описывает вашу практику в OpenMyMind. Сервер хранит категории результатов и даты. Тексты вопросов и ответов остаются вне его базы. После отключения статистики новые результаты перестают записываться, а накопленные остаются доступны.

Попробуйте запрос **«Покажи мой прогресс в OpenMyMind за последние 7 дней»**.

### Настройте почтовые напоминания

Подключите аккаунт с подтверждённым адресом электронной почты. Попросите OpenMyMind напоминать о тренировке **ежедневно** или **раз в три дня**. Первое письмо планируется через выбранный интервал. Частоту можно изменить в чате. Чтобы прекратить письма, попросите об этом в чате или воспользуйтесь ссылкой в письме.

Попробуйте запрос **«Напоминай мне о тренировке раз в три дня»**.

### Настройка и язык

Тренировочные режимы можно запустить в ChatGPT как плагин на основе навыка. Для статистики и собственных писем OpenMyMind нужно подключить MCP-сервер. Текущая сборка запускает MCP-сервер на Python и обработчик писем отдельными процессами. См. [инструкцию по развёртыванию](#развёртывание-сервера). Плагин отвечает на вашем языке. Графики и письма в текущей версии оформлены на английском.

## Қазақша

OpenMyMind — ChatGPT плагині. Ол модельдің түсіндірмесін оқымас бұрын өз жауабыңызды тұжырымдауға уақыт береді. Оны жаңа ұғымды түсіну, болжамды тексеру немесе өз ойыңызды түсіндіріп жаттығу үшін қолданыңыз.

<img width="1672" height="941" alt="Think_yourself_first" src="https://github.com/user-attachments/assets/510e49a5-1b55-47ab-b364-461bfbe381a9" />

### Жаттығуды бастау

1. OpenMyMind плагинін ChatGPT-ге орнатып, жаңа чат ашыңыз.
2. `@OpenMyMind` плагинін таңдап, сұрақ қойыңыз. Режимді сұрақпен бірге атай аласыз немесе ұсынылған нұсқалардың бірін таңдай аласыз.
3. Өз ойыңызды айтыңыз, тест жауабын таңдаңыз немесе кез келген сәтте дайын жауапты сұраңыз.

| Режим | Жаттығу қалай өтеді | Сұрау үлгісі |
| --- | --- | --- |
| **Жетелеуші сұрақтар** | Плагин 3–5 ашық сұрақ қойып, жауабыңызды күтеді. Бір сұраққа жауап берсеңіз жеткілікті. Плагин ойыңызды талдап, тікелей жауап береді және негізгі қорытындыны қалай тексеруге болатынын түсіндіреді. Қаласаңыз, ишара сұраңыз. | «Git-те тармақтар не үшін керек екенін жетелеуші сұрақтар арқылы түсінуге көмектес». |
| **Қысқа тест** | Үш нұсқаның бірін таңдаңыз. Дұрыс таңдасаңыз, плагин жауапты тереңірек түсіндіреді. Қателессеңіз, таңдаған нұсқадағы нақты қатені көрсетіп, дұрыс жауапқа қалай келуге болатынын түсіндіреді. | «Маған логика бойынша қысқа тест бер». |
| **Өз болжамыңызды ұсыныңыз** | Алдымен өз жауабыңызды айтыңыз. Жауабыңыз дұрыс тұжырымға жақын болса, плагин қай тұсын дұрыс байқағаныңызды айтып, түсіндірмені толықтырады. Елеулі олқылық болса, оны көрсетіп, қайта байқап көруді, режимді ауыстыруды немесе дайын жауап алуды ұсынады. | «Мұздың неге су бетінде қалқитыны туралы өз болжамымды айтқым келеді». |

### Ілгерілеуді бақылау

OpenMyMind тіркелгіңізді байланыстырып, статистика жинауды бөлек қосыңыз. Содан кейін соңғы **7 күн**, **30 күн** немесе **барлық уақыт** бойынша есеп сұраңыз. Есепте өз бетіңізше берген жауаптар, жетелеуші сұрақтардан кейін берген жауаптар және жаттығуға кіріспей сұраған дайын жауаптар саналады. Тест нәтижелері мен жаттығуды бастағаннан кейін сұралған дайын жауаптар бөлек көрсетіледі.

График тесттен тыс аяқталған жаттығулардың ішінде өз бетіңізше жауап бергендерінің үлесін көрсетеді. 7 және 30 күндік есептерде нәтижелер UTC бойынша күнге, ал барлық уақыт бойынша есепте айға топтастырылады. Бұл көрсеткіш OpenMyMind ішіндегі жаттығуларыңызды сипаттайды. Сервер нәтиженің санаты мен уақытын сақтайды. Сұрақтар мен жауаптардың мәтіні дерекқорға жазылмайды. Статистиканы өшірсеңіз, жаңа нәтижелер тіркелмейді, бұрынғы нәтижелер сақталады.

Мысалы, **«OpenMyMind-тағы соңғы 7 күндегі нәтижелерімді көрсет»** деп жазыңыз.

### Электрондық пошта еске салғыштарын баптау

Электрондық пошта мекенжайы расталған тіркелгіні байланыстырыңыз. OpenMyMind-тан жаттығуды **күн сайын** немесе **үш күнде бір рет** еске салуын сұраңыз. Алғашқы хат таңдалған аралық өткеннен кейін жіберіледі. Жиілігін чатта өзгерте аласыз. Хаттарды тоқтату үшін чатта сұраңыз немесе хаттағы сілтемені пайдаланыңыз.

Мысалы, **«Жаттығуды үш күнде бір рет еске сал»** деп жазыңыз.

### Баптау және тіл

Жаттығу режимдерін ChatGPT-де дағдыға негізделген плагин ретінде іске қосуға болады. Статистика мен OpenMyMind жіберетін хаттар үшін MCP серверін қосу қажет. Қазіргі нұсқада Python тіліндегі MCP сервері мен хат жіберетін бағдарлама бөлек процесс ретінде іске қосылады. Төмендегі [серверді орнату нұсқаулығын](#развёртывание-сервера) қараңыз. Плагин сіздің тіліңізде жауап береді. Қазіргі нұсқада графиктер мен еске салу хаттары ағылшын тілінде.

## Развёртывание сервера

Текущая сборка OpenMyMind рассчитана на отдельный запуск MCP-сервера на Python и обработчика почтовых напоминаний.

Требуются Python 3.12, публичный HTTPS-адрес, провайдер OAuth и SMTP-сервис для отправки писем. Установите зависимости из корня распакованного архива.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Храните переменные окружения и секреты в конфигурации сервера. Сервер MCP и обработчик писем должны работать с одной базой на постоянном диске.

| Переменная | Значение |
| --- | --- |
| `OPENMYMIND_MCP_URL` | Публичный HTTPS-адрес, который оканчивается на `/mcp` |
| `OPENMYMIND_ISSUER` | Точный issuer провайдера, включая завершающий слеш, если он есть в токене |
| `OPENMYMIND_JWKS_URL` | HTTPS-адрес публичных ключей провайдера |
| `OPENMYMIND_CLIENT_ID` | Идентификатор OAuth-клиента, зарегистрированного для подключения ChatGPT |
| `OPENMYMIND_DB` | Абсолютный путь к SQLite-файлу на постоянном диске |
| `OPENMYMIND_EMAIL_CLAIM`, `OPENMYMIND_EMAIL_VERIFIED_CLAIM` | Названия полей в access token. По умолчанию `email` и `email_verified` |
| `OPENMYMIND_SMTP_HOST`, `OPENMYMIND_SMTP_PORT` | SMTP-хост и порт. По умолчанию порт 465 |
| `OPENMYMIND_SMTP_TLS` | `implicit` для TLS при подключении или `starttls` для STARTTLS |
| `OPENMYMIND_SMTP_USERNAME`, `OPENMYMIND_SMTP_PASSWORD` | Данные SMTP-сервиса, если он требует вход |
| `OPENMYMIND_FROM` | Подтверждённый адрес отправителя |

Настройте OAuth Authorization Code с PKCE, стандартной метаинформацией провайдера и поддержкой параметра `resource`. Зарегистрируйте callback, показанный ChatGPT в процессе подключения. Access token должен быть JWT с подписью RS256, сроком действия, `iss`, стабильным `sub`, `aud` со значением публичного `/mcp`, строковым `scope` со значением `openmymind` и `client_id` или `azp`. Для напоминаний провайдер должен включать утверждения о подтверждённом адресе именно в access token. Проверьте также обновление токенов у вашего провайдера. [Документация OpenAI по авторизации](https://developers.openai.com/plugins/build/auth).

За HTTPS-прокси запустите команду ниже. Прокси должен сохранять публичный заголовок Host и передавать запросы к `/mcp`, `/.well-known/oauth-protected-resource/mcp` и `/unsubscribe/`.

```bash
python -m uvicorn openmymind.server:app --factory --host 127.0.0.1 --port 8000 --no-access-log
```

Запускайте команду обработки писем каждую минуту через cron, systemd timer или планировщик хостинга. Передайте ей те же переменные окружения, включая SMTP и путь к базе.

```bash
python -m openmymind.worker
```

Обработчик выбирает готовые к отправке напоминания и планирует следующую отправку. При ошибках SMTP он откладывает повторную попытку. Если провайдер примет письмо, но соединение оборвётся до подтверждения, повторная попытка может привести к дубликату. Отключите запись путей отписки и заголовков авторизации в логах прокси.

## Сборка пакета для ChatGPT

Соберите отдельный ZIP для развёрнутого MCP-сервера. Подставьте свой адрес и публичный OAuth client ID. Если провайдер использует другой способ аутентификации клиента, укажите его через `--token-auth`. Секрет клиента задаётся в настройках подключения.

```bash
python build_plugin.py --url https://your-domain.example/mcp --client-id YOUR_CLIENT_ID
```

Результат — `OpenMyMind-v2-plugin.zip` с манифестом, навыком и конфигурацией MCP. Подключите и проверьте свой сервер в ChatGPT до отправки на модерацию. Для публичной версии используйте подачу **With MCP**. Если предыдущая версия была подана как **Skills only**, создайте новую заявку для версии с MCP. [Руководство по подключению](https://developers.openai.com/plugins/deploy/connect-chatgpt) · [Руководство по публикации](https://developers.openai.com/plugins/deploy/submission).

Перед публикацией проверьте в новом чате все три режима и прямой ответ, затем подключите тестовый аккаунт, запросите три отчёта, проверьте доставку письма на тестовый адрес и отписку.

