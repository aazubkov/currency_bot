# currency_bot
Telegram bot on telebot library. Bot parses currency rates and kindly converts one into another. Usefull thing.
As usual base code was given in the SkillFactory presentation. And as usual I tried to make small updates.
# Updates
1) Added command menu list with number of usefull commands.
2) Integrated cryptocurrency into converter. Exchangerate service was used: https://exchangerate.host
3) Included an HTML mode in sent messages. No functionality. Just for a bit more esthtic)
4) Fixed a small kosyak in presentation code while using register_next_step_handler(). User used to start from begining of Converting process as if he entered incorrect amount (at the last step). In this version, User is sent back to amount request and don't need to start all Convert dialog from the begining. Useability dramatically increased. Oh yeah.
