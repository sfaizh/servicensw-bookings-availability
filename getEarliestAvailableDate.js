const Nightmare = require('nightmare')
const nightmare = Nightmare()
nightmare
  .goto('https://www.myrta.com/wps/portal/extvp/myrta/licence/tbs/tbs-change/!ut/p/b1/lc7fboIwFAbwZ_EBTP8p1MsiCN1EECyD3hBWWIODmm2OuLcf3pg')
  .type('#widget_input_bookingId', '15855885')
  .type('#widget_input_familyName', 'HUSSAIN')
  .click('#submitNoLogin')
  .wait('#changeTimeButton_label')
  .click('#changeTimeButton_label')
  .wait('#getEarliestTime')
  .click('#getEarliestTime')
  .wait(6000)
  .evaluate(() => {
      var availableSlotClass = document.querySelector(".available").parentNode.className;
      var availableDate = document.querySelector("."+availableSlotClass);
      var availableSlot = document.querySelector(".available").parentNode;

      var time = availableSlot.childNodes[0].innerHTML;
      var date = availableDate.childNodes[0].childNodes[0].innerHTML;
      return date + "|" + time;
  })
  .end()
  .then((response) => {
    console.log(response);
  })
  .catch(error => {
    console.error('Search failed:', error)
  })
