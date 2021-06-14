titTxt = document.querySelector("#title").value
subTitTxt = document.querySelector("#subtitle").value

textCounter(subTitTxt, "#sub-tit-txt-cnt")
textCounter(titTxt, "#tit-txt-cnt")

function subTitTxtCnt(txt) {
  textCounter(txt, "#sub-tit-txt-cnt")
}
function TitTxtCnt(txt) {
  textCounter(txt, "#tit-txt-cnt")
}

function textCounter(txt, id) {
  if (txt.length < 10) {
    document.querySelector(id).innerHTML = "00" + txt.length
  } else if (txt.length < 100) {
    document.querySelector(id).innerHTML = "0" + txt.length
  }
  else {
    document.querySelector(id).innerHTML = txt.length
  }
}