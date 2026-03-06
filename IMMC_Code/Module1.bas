Attribute VB_Name = "Module1"
Option Explicit

Function nCr(n As Long, r As Long) As Long
Dim res As Long, i As Long, temp As Double
    temp = 1
    For i = 1 To r: temp = temp * (n - r + i) / i: Next i
    nCr = Round(temp)
End Function

Sub GetCombosNoRep(ByRef combos() As Long, n As Long, r As Long, numRows As Long)

Dim index() As Long
Dim numIter As Long, i As Long, k As Long, count As Long

    ReDim index(1 To r)
    count = 1
    For i = 1 To r: index(i) = i: Next

    While count <= numRows
        numIter = n - index(r) + 1

        For i = 1 To numIter
            For k = 1 To r
                combos(count, k) = index(k)
            Next k
            count = count + 1
            index(r) = index(r) + 1
        Next i

        For i = r - 1 To 1 Step -1
            If index(i) <> (n - r + i) Then
                index(i) = index(i) + 1
                For k = i + 1 To r
                    index(k) = index(k - 1) + 1
                Next k

                Exit For
            End If
        Next i
    Wend

End Sub

Sub GetComplement(n As Long, childVec() As Long, complementVec() As Long)

Dim i As Long, j As Long

    ReDim logicalVec(1 To n)
    For i = 1 To n: logicalVec(i) = True: Next i
    For i = 1 To UBound(childVec): logicalVec(childVec(i)) = False: Next i
    j = 1

    For i = 1 To n
        If logicalVec(i) Then
            complementVec(j) = i
            j = j + 1
        End If
    Next i

End Sub

Sub MasterGenerator()

Dim myRows As Long, i As Long, j As Long, r As Long, n As Long
Dim combos() As Long, k As Long, gSize As Long, total As Long
Dim sTime As Double, eTime As Double, verbose As Boolean

    n = CLng(InputBox("How many datasets do you have?", "ENTER # OF DATASETS", "16"))
    r = CLng(InputBox("How many groups do you have?", "ENTER # OF GROUPS", "4"))
    verbose = CBool(InputBox("Should the results be printed?", "VERBOSE OPTION", "True"))

    If Abs(Round(n / r) - (n / r)) > 0.00001 Or r < 2 Or r >= n Then
        MsgBox "Incorrect input!!!"
        '' You could have custom message like: MsgBox "# of Datasets is NOT divisible by # of Groups!!!"
        Exit Sub
    End If

    sTime = Timer
    gSize = n / r
    total = 1

    Dim AllCombs() As Variant, tN As Long
    ReDim AllCombs(1 To r - 1)
    tN = n

    For i = 1 To r - 1
        myRows = nCr(tN, gSize)
        ReDim combos(1 To myRows, 1 To gSize)
        Call GetCombosNoRep(combos, tN, gSize, myRows)
        total = total * myRows / (r - (i - 1))
        AllCombs(i) = combos
        tN = tN - gSize
    Next i

    Dim MasterGroups() As Long
    ReDim MasterGroups(1 To total, 1 To r, 1 To gSize)

    Dim secLength As Long, s As Long, e As Long, m As Long
    secLength = nCr(n, gSize) / r

    Dim v() As Long, child() As Long, q As Long, temp As Long
    ReDim v(1 To n)
    For i = 1 To n: v(i) = i: Next i

    ReDim child(1 To gSize)
    Dim superSecLen As Long, numReps As Long
    superSecLen = total
    Dim endChild() As Long, endV() As Long
    ReDim endChild(1 To n - gSize)
    ReDim endV(1 To gSize)

    '' Populate all but the last 2 columns
    If r > 2 Then
        For i = 1 To r - 2
            numReps = nCr(n - (i - 1) * gSize, gSize) / (r - (i - 1))
            secLength = superSecLen / numReps
            s = 1: e = secLength

            If i = 1 Then
                For j = 1 To numReps
                    For k = s To e
                        For m = 1 To gSize
                            MasterGroups(k, i, m) = v(AllCombs(i)(j, m))
                        Next m
                    Next k
                    s = e + 1
                    e = e + secLength
                Next j
            Else
                ReDim child(1 To (i - 1) * gSize)
                ReDim v(1 To n - (i - 1) * gSize)

                While e < total
                    '' populate child vector so we can get the complement
                    For j = 1 To i - 1
                        For m = 1 To gSize
                            child(m + (j - 1) * gSize) = MasterGroups(s, j, m)
                        Next m
                    Next j

                    Call GetComplement(n, child, v)

                    For q = 1 To numReps
                        For k = s To e
                            For m = 1 To gSize
                                MasterGroups(k, i, m) = v(AllCombs(i)(q, m))
                            Next m
                        Next k
                        s = e + 1
                        e = e + secLength
                    Next q
                Wend
            End If

            superSecLen = secLength
        Next i

        numReps = nCr(n - (r - 2) * gSize, gSize) / (r - 2)
        s = 1: e = secLength

        ReDim child(1 To (r - 2) * gSize)
        ReDim v(1 To n - (r - 2) * gSize)

        While e <= total
            '' populate child vector so we can get the complement
            For j = 1 To r - 2
                For m = 1 To gSize
                    child(m + (j - 1) * gSize) = MasterGroups(s, j, m)
                    endChild(m + (j - 1) * gSize) = MasterGroups(s, j, m)
                Next m
            Next j

            Call GetComplement(n, child, v)
            q = 1

            For k = s To e
                For m = 1 To gSize
                    MasterGroups(k, r - 1, m) = v(AllCombs(r - 1)(q, m))
                    endChild(m + (r - 2) * gSize) = MasterGroups(k, r - 1, m)
                Next m

                q = q + 1
                Call GetComplement(n, endChild, endV)

                For m = 1 To gSize
                    MasterGroups(k, r, m) = endV(m)
                Next m
            Next k
            s = e + 1
            e = e + secLength
        Wend
    Else
        For k = 1 To total
            For m = 1 To gSize
                MasterGroups(k, 1, m) = v(AllCombs(1)(k, m))
                endChild(m) = MasterGroups(k, 1, m)
            Next m

            Call GetComplement(n, endChild, endV)

            For m = 1 To gSize
                MasterGroups(k, 2, m) = endV(m)
            Next m
        Next k
    End If

    If verbose Then
        Dim myString As String, totalString As String, printTotal As Long
        printTotal = Application.WorksheetFunction.Min(100000, total)

        For i = 1 To printTotal
            totalString = vbNullString
            For j = 1 To r
                myString = vbNullString
                For k = 1 To gSize
                    myString = myString & " " & MasterGroups(i, j, k)
                Next k
                myString = Right(myString, Len(myString) - 1)
                myString = "(" & myString & ") "
                totalString = totalString + myString
            Next j
            Cells(i, 1) = totalString
        Next i
        eTime = Timer - sTime
        MsgBox "Generation of " & total & " as well as printing " & printTotal & " custom combinations  completed in : " & eTime & " seconds"
    Else
        eTime = Timer - sTime
        MsgBox "Generation of " & total & " custom combinations completed in : " & eTime & " seconds"
    End If

End Sub
