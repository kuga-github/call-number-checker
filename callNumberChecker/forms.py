from django import forms
import unicodedata
import re

from .models import RecordID
from .scraping import scraping

class ContactForm(forms.Form):
  record_id = forms.CharField(label="資料ID")

  def clean(self):
    cleaned_data = super().clean()
    text = cleaned_data.get("record_id")

    if isEmpty(text):
      raise forms.ValidationError("13桁の半角数字を入力してください。")
    
    elif len(text) != 13 or isHalfNum(text) != True:
      raise forms.ValidationError("13桁の半角数字を入力してください。")

    if RecordID.objects.filter(record_id=text):
      raise forms.ValidationError("資料ID:{}は登録済みです。".format(text))

    info = scraping(text)
    if info["is_right_id"] != True:
      raise forms.ValidationError("資料ID:{}は存在しません。".format(text))
    
    cleaned_data["cTop"] = info["cTop"]
    cleaned_data["cMdl"] = info["cMdl"]
    cleaned_data["cBtm"] = info["cBtm"]
    
    return cleaned_data

  def save(self):
    data = self.cleaned_data
    recordid = RecordID(
      record_id = data["record_id"],
      cTop = data["cTop"],
      cMdl = data["cMdl"],
      cBtm = data["cBtm"],
      is_right_callNumber = isRightCallNumber(data["cTop"], data["cMdl"], data["cBtm"])
      )
    recordid.save()

def isHalfNum(str):
    try:
      int(str)
    except ValueError:
      return False
    for char in str:
      if 'Na' != unicodedata.east_asian_width(char):
        return False
    return True

def isEmpty(str):
  try:
    len(str)
  except TypeError:
    return True
  return False

def isRightCallNumber(cTop, cMdl, cBtm):
  d = {'　': ''}
  tbl = str.maketrans(d)
  ctop = cTop.translate(tbl)
  cmdl = cMdl.translate(tbl)

  if len(ctop) > 0 and len(cmdl) > 0:
    p = re.compile('[a-zA-Z]+')
    rectop = "".join(re.findall(p,ctop))
    recmdl = "".join(re.findall(p,cmdl))

    if rectop == ctop or recmdl == cmdl:
      p = re.compile('[0-9.]+')
      rectop = "".join(re.findall(p,ctop))
      recmdl = "".join(re.findall(p,cmdl))
      if rectop == ctop or recmdl == cmdl:
        return True
  return False