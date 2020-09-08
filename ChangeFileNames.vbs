'----------Created by Brandon Rumer--------------------------
'------------------------------------------------------------
'------------------------------------------------------------
'---Change the line below to the desired folder directory----
'------------------------------------------------------------

strFolder="C:\file\stuff"

'------------------------------------------------------------
'------------------------------------------------------------
'------------------------------------------------------------
'---------DO NOT MODIFY ANYTHING BELOW THIS LINE-------------


Set objFS = CreateObject("Scripting.FileSystemObject")
Set objFolder = objFS.GetFolder(strFolder)


'Removes items in Brackets
For Each strFile In objFolder.Files
		strFileName = strFile.Name
		If InStr(strFileName,"]") > 0 Then		  
		  s= Split(strFileName,"]")
		  For i=LBound(s) To UBound(s)
		    index=InStr(s(i),"[")
		    If index>0 Then
		      s(i)=Mid(s(i),1,index-1)
		    End If 
		  Next		  
		End If	  	   	 
		strFile.Name=Join(s,"") 
Next 


'Removes items in Parentheses
For Each strFile In objFolder.Files
		strFileName = strFile.Name
		If InStr(strFileName,")") > 0 Then		  
		  s= Split(strFileName,")")
		  For i=LBound(s) To UBound(s)
		    index=InStr(s(i),"(")
		    If index>0 Then
		      s(i)=Mid(s(i),1,index-1)
		    End If 
		  Next		  
		End If	  	   	 
		strFile.Name=Join(s,"") 
Next 



'Removes OBJ
For Each strFile In objFolder.Files

		strFileName = strFile.Name
		If instr(ucase(strFile.Name),"OBJ") Then		  
		  dname=replace(strFile.Name,"OBJ","")
		  strFile.move objFolder & "\" & dname 
		End If
Next 



'Removes Special Characters
For Each strFile In objFolder.Files
	strFileName = strFile.Name
	theString = strFileName
'	wscript.echo strFileName & " strFileName"
	
	strAlphaNumeric = "[^a-zA-Z0-9. "
		For i = 1 to len(theString) 
		strChar = mid(theString,i,1) 
			If instr(strAlphaNumeric,strChar) Then 
				CleanedString = CleanedString & strChar 
				End If 
		Next 
'	wscript.echo cleanedstring & " cleanedstring"
	CleanTheString = CleanedString
	strFile.move objFolder & "\" & CleanedString
	CleanTheString = ""
	CleanedString = ""
Next 



'Removes CORRECTION
For Each strFile In objFolder.Files

		strFileName = strFile.Name
		If instr(ucase(strFile.Name),"CORRECTION") Then		  
		  dname=replace(strFile.Name,"CORRECTION","")
		  strFile.move objFolder & "\" & dname 
		End If
Next 


'Removes CORRECTED
For Each strFile In objFolder.Files

		strFileName = strFile.Name
		If instr(ucase(strFile.Name),"CORRECTED") Then		  
		  dname=replace(strFile.Name,"CORRECTED","")
		  strFile.move objFolder & "\" & dname 
		End If
Next 



'Adds Done to begenning of file name
For Each strFile In objFolder.Files

		strFileName = strFile.Name
		If instr(ucase(strFile.Name),"Done") Then
			wscript.echo "File already has Done in the name" 
		else
			strFile.move objFolder & "\" & "Done " & strFileName
		End If

Next 



