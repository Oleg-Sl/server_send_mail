<?php
    global $APPLICATION;
    out($APPLICATION->GetCurPage());
    out($_REQUEST);
?>

<!DOCTYPE html>
<html>
  <head>
    <base target="_top">
  </head>
  <body>
    <div id="name"></div>
    <input type="button" id="button" value="Кнопка">
    <script src="//api.bitrix24.com/api/v1/"></script>
    <script>
        BX24.init(async () => {
            let button = document.getElementById('button');
            BX24.placement.bindEvent('CallCard::BeforeClose', () => {
                console.log("CallCard::BeforeClose = ")
            });

            button.addEventListener('click', async (e) => {
                console.log("Нажали кнопку!");

                  BX24.placement.call('getStatus', {}, (res) => {
                      console.log("CALL_CARD getStatus = ", res);
                  })
                  console.log(BX24.getPath);
                  BX24.callMethod('methods', {scope: "placement"}, (data) => {
                      console.log("methods = ", data);
                  });
                  BX24.callMethod('events', {scope: "placement"}, (data) => {
                      console.log("events = ", data);
                  });
                  let addr = await BX24.getDomain();
                  console.log("addr = ", addr);
            })

        })
    </script>
  </body>
</html>