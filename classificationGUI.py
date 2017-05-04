try:
    # python 2 module
    import Tkinter as tk
    import ttk as ttk
    import arcpy
    import datetime
    import os.path
    from inspect import currentframe, getframeinfo
except ImportError:
    #python 3 module
    import tkinter as tk
    import ttk as ttk
    import arcpy
    import datetime
    import os.path
    from inspect import currentframe, getframeinfo
except Exception as e:
    arcpy.AddMessage(e)


# Logistics --------------------------------------------------------------------
errorLog = []
errorLogPath = r'C:\MBNEP\Wetlands Classification Script\Error Log.txt'


def preWrite(*args):

    nullWrite = ivNullBox.get()
    modWrite = ivModBox.get()
    userSystem = svSystem.get()
    userSubsystem = svSubsystem.get()
    userClass = svClass.get()
    userSubclass = svSubclass.get()
    userModifiers = svModifiers.get()

    if nullWrite:
        if modWrite:
            if len(userModifiers) > 1:
                write()
            else:
                arcpy.AddMessage("[Force Modifiers] is enabled. Provide a modification to continue, or toggle this setting.")
        else:
            write()
    else:
        if modWrite:
            if (len(userSystem) > 1 and len(userSubsystem) > 1 and
                len(userClass) > 1 and len(userSubclass) > 1 and
                len(userModifiers) > 1):
                write()
            else:
                arcpy.AddMessage("[Force Modifiers] is enabled. Provide a modification to continue, or toggle this setting.")
        else:
            if (len(userSystem) > 1 and len(userSubsystem) > 1 and
                len(userClass) > 1 and len(userSubclass) > 1):
                write()
            else:
                arcpy.AddMessage("[Allow Emtpy Writes] is disabled. Provide a value for each classification level, or toggle this setting.")


# Data Frame Write -------------------------------------------------------------
def write():

    global sc
    global lc

    try:
        cursor = arcpy.UpdateCursor(currentLayer)
    except Exception as e:
        arcpy.AddMessage(e)

    # Ensure field lengths are not exceeded.
    sysLen = None
    subsysLen = None
    classLen = None
    subclassLen = None
    modLen = None
    habLen = None

    try:
        fields = arcpy.ListFields(currentLayer)
        for field in fields:
            if field.name == "System":
                sysLen = field.length
            elif field.name == "Subsystem":
                subsysLen = field.length
            elif field.name == "Class":
                classLen = field.length
            elif field.name == "Subclass":
                subclassLen = field.length
            elif field.name == "Modifier":
                modLen = field.length
            elif field.name == "HABITAT":
                habLen = field.length
            ## DEBUG: Use when someone changes the column names
            # arcpy.AddMessage(field.name)
    except Exception as e:
        arcpy.AddMessage(e)

    try:
        for row in cursor:
            try:
                if len(lc[0]) <= sysLen:
                    row.setValue("System", lc[0])
                else:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[line {2}] Failed to write [{0}]. The maximum length that can be written to this field is: {1}".format(lc[0], sysLen, frameinfo.lineno)
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)
            except Exception as a:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[line {2}] Failed to write [{0}]. The column name has likely been changed. Expected column name: [{1}]".format(lc[0], "System", frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)
            try:
                if len(lc[1]) <= subsysLen:
                    row.setValue("Subsystem", lc[1])
                else:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[line {2}] Failed to write [{0}]. The maximum length that can be written to this field is: {1}".format(lc[1], subsysLen, frameinfo.lineno)
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)
            except Exception as b:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[line {2}] Failed to write [{0}]. The column name has likely been changed. Expected column name: [{1}]".format( lc[1], "Subsystem", frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)
            try:
                if len(lc[2]) <= classLen:
                    row.setValue("Class", lc[2])
                else:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[line {2}] Failed to write [{0}]. The maximum length that can be written to this field is: {1}".format(lc[2], classLen, frameinfo.lineno)
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)
            except Exception as c:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[line {2}] Failed to write [{0}]. The column name has likely been changed. Expected column name: [{1}]".format( lc[2], "Class", frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)
            try:
                if len(lc[3]) <= subclassLen:
                    row.setValue("Subclass", lc[3])
                else:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[line {2}] Failed to write [{0}]. The maximum length that can be written to this field is: {1}".format(lc[3], subclassLen, frameinfo.lineno)
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)
            except Exception as d:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[line {2}] Failed to write [{0}]. The column name has likely been changed. Expected column name: [{1}]".format( lc[3], "Subclass", frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)
            try:
                if len(lc[4]) <= modLen:
                    row.setValue("Modifier", lc[4])
                else:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[line {2}] Failed to write [{0}]. The maximum length that can be written to this field is: {1}".format(lc[4], modLen, frameinfo.lineno)
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)
            except Exception as f:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[line {2}] Failed to write [{0}]. The column name has likely been changed. Expected column name: [{1}]".format( lc[4], "Modifier", frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

            sctemp = []
            scFinal = []

            # The user may try to write all "N/A" values,
            # in which case this section will fail.
            try:
                for i in sc:
                    if i != "N/A":
                        sctemp.append(i)

                scFinal = "".join(sctemp)
            except:
                scFinal = "N/A"

            try:
                row.setValue("HABITAT", scFinal)
            except Exception as g:
                if len(scFinal) <= habLen:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[line {2}] Failed to write [{0}]. 2 Errors Found. [Error 1/2] The maximum length that can be written to this field is: {1}. [Error 2/2] The column, frameinfo.lineno name has likely been changed. Expected column name: [{2}]".format(scFinal, habLen, "HABITAT")
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)
                else:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[line {2}] Failed to write [{0}]. The column name has likely been changed. Expected column name: [{1}]".format(scFinal, "HABITAT", frameinfo.lineno)
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)

            cursor.updateRow(row)

    except Exception as e:
        arcpy.AddMessage(e)

    del cursor

    # Write data log, if user chooses to.
    logErrors = ivErrorBox.get()
    if logErrors:
        try:
            with open(errorLogPath, 'a') as f:
                # Log header
                f.write('\n')
                now = datetime.datetime.now()
                header = ('Log Created: ' + str(now.month) + '/' + str(now.day)
                    + '/' + str(now.year) + '\n' + '------------------------\n')
                f.write(header)
                for error in errorLog:
                    f.write(error + '\n')
                f.close()
        except FileNotFoundError:
            with open(errorLogPath, 'w') as f:
                f.close()
            with open(errorLogPath, 'a') as f:
                # Log header
                f.write('\n')
                now = datetime.datetime.now()
                header = ('Log Created: ' + str(now.month) + '/' + str(now.day)
                    + '/' + str(now.year) + '\n' + '------------------------\n')
                f.write(header)
                for error in errorLog:
                    f.write(error + '\n')
                f.close()
        except Exception as z:
            arcpy.AddMessage(z)


# List Build Logic -------------------------------------------------------------
def displayClassifications(lc, sc):
    lctemp = []
    sctemp = []
    lcFinal = []
    scFinal = []

    # DEBUG:
    # arcpy.AddMessage("lc: {0}".format(lc))
    # arcpy.AddMessage("sc: {0}".format(sc))

    for i in lc:
        if i != "N/A":
            lctemp.append(i)

    for i in sc:
        if i != "N/A":
            sctemp.append(i)

    lcFinal = " | ".join(lctemp)
    scFinal = "".join(sctemp)

    longClassification.set(lcFinal)
    shortClassification.set(scFinal)


def eSystem(*args):

    global cboxSystem
    global cboxSubsystem
    global cboxClass
    global cboxSubclass
    global cboxModifiers

    global dictSystem
    global dictSubsystem
    global dictClass
    global dictSubclass
    global dictModifiers

    global lc
    global sc

    if len(dictSubsystem) > 0:

        # Clear all lower echelon comboboxes/selections
        # Reset selections
        svSubsystem.set('')
        svClass.set('')
        svSubclass.set('')
        svModifiers.set('')

        # Reset global tracking variables
        dictSubsystem = []
        dictClass = []
        dictSubclass = []
        dictModifiers = []

        # Delete lists
        cboxSubsystem['menu'].delete(0, 'end')
        cboxClass['menu'].delete(0, 'end')
        cboxSubclass['menu'].delete(0, 'end')
        cboxModifiers['menu'].delete(0, 'end')

        # Clean up Short & Long Classifications
        for i in range(0, len(lc)):
            lc[i] = "N/A"
        for i in range(0, len(sc)):
            sc[i] = "N/A"

    # Build new selections
    userSystem = svSystem.get()
    if len(userSystem) > 1:

        if (userSystem == "Marine") or (userSystem == "Estuarine"):
            dictSubsystem = ['Subtidal', 'Intertidal']
            for choice in dictSubsystem:
                cboxSubsystem['menu'].add_command(label = choice,
                    command = tk._setit(svSubsystem, choice))
            if userSystem == "Marine":
                lc[0] = "Marine"
                sc[0] = "M"
            else:
                lc[0] = "Estuarine"
                sc[0] = "E"
            displayClassifications(lc, sc)

        elif userSystem == "Lacustrine":
            dictSubsystem = ['Limnetic', 'Littoral']
            for choice in dictSubsystem:
                cboxSubsystem['menu'].add_command(label = choice,
                    command = tk._setit(svSubsystem, choice))

            lc[0] = "Lacustrine"
            sc[0] = "L"
            displayClassifications(lc, sc)

        elif userSystem == "Palustrine":
            dictSubsystem = ['Not Applicable']
            for choice in dictSubsystem:
                cboxSubsystem['menu'].add_command(label = choice,
                    command = tk._setit(svSubsystem, choice))

            lc[0] = "Palustrine"
            sc[0] = "P"
            displayClassifications(lc, sc)

        elif userSystem == "Riverine":
            dictSubsystem = ['Tidal', 'Lower Perennial', 'Upper Perennial',
                'Intermittent', 'Unknown Perennial']
            for choice in dictSubsystem:
                cboxSubsystem['menu'].add_command(label = choice,
                    command = tk._setit(svSubsystem, choice))

            lc[0] = "Riverine"
            sc[0] = "R"
            displayClassifications(lc, sc)

        elif userSystem == "Upland":
            dictSubsystem = ['Urban', 'Agriculture', 'Range', 'Forest', 'Barren']
            for choice in dictSubsystem:
                cboxSubsystem['menu'].add_command(label = choice,
                    command = tk._setit(svSubsystem, choice))

            lc[0] = "Upland"
            sc[0] = "U"
            displayClassifications(lc, sc)

        else:
            frameinfo = getframeinfo(currentframe())
            errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a System".format((longClassification.get() + " | " + "[" + userSystem + "]"), userSystem, frameinfo.lineno)
            arcpy.AddMessage(errorMessage)
            errorLog.append(errorMessage)

def eSubsystem(*args):

    global cboxSubsystem
    global cboxClass
    global cboxSubclass
    global cboxModifiers

    global dictSubsystem
    global dictClass
    global dictSubclass
    global dictModifiers

    global lc
    global sc

    if len(dictClass) > 0:

        # Clear all lower echelon comboboxes/selections
        # Reset selections
        svClass.set('')
        svSubclass.set('')
        svModifiers.set('')

        # Reset global tracking variables
        dictClass = []
        dictSubclass = []
        dictModifiers = []

        # Delete lists
        cboxClass['menu'].delete(0, 'end')
        cboxSubclass['menu'].delete(0, 'end')
        cboxModifiers['menu'].delete(0, 'end')

        # Clean up Short & Long Classifications
        for i in range(1, len(lc)):
            lc[i] = "N/A"
        for i in range(1, len(sc)):
            sc[i] = "N/A"

    # Build new selections
    userSystem = svSystem.get()
    userSubsystem = svSubsystem.get()
    if len(userSystem) > 1 and len(userSubsystem) > 1:

        if userSystem == "Marine":

            if userSubsystem == "Subtidal":
                dictClass = ['Rock Bottom', 'Unconsolidated Bottom',
                    'Aquatic Bed', 'Reef']
                for choice in dictClass:
                    cboxClass['menu'].add_command(label = choice,
                        command = tk._setit(svClass, choice))

                lc[1] = "Subtidal"
                sc[1] = "1"
                displayClassifications(lc, sc)

            elif userSubsystem == "Intertidal":
                dictClass = ['Aquatic Bed', 'Reef', 'Rocky Shore',
                    'Unconsolidated Shore']
                for choice in dictClass:
                    cboxClass['menu'].add_command(label = choice,
                        command = tk._setit(svClass, choice))

                lc[1] = "Intertidal"
                sc[1] = "2"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subsystem".format((longClassification.get() + " | " + "[" + userSubsystem + "]"), userSubsystem, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userSystem == "Estuarine":

            if userSubsystem == "Subtidal":
                dictClass = ['Rock Bottom', 'Unconsolidated Bottom',
                    'Aquatic Bed', 'Reef']
                for choice in dictClass:
                    cboxClass['menu'].add_command(label = choice,
                        command = tk._setit(svClass, choice))

                lc[1] = "Subtidal"
                sc[1] = "1"
                displayClassifications(lc, sc)

            elif userSubsystem == "Intertidal":
                dictClass = ['Aquatic Bed', 'Reef', 'Streambed', 'Rocky Shore',
                    'Unconsolidated Shore', 'Emergent', 'Scrub-Shrub', 'Forested']
                for choice in dictClass:
                    cboxClass['menu'].add_command(label = choice,
                        command = tk._setit(svClass, choice))

                lc[1] = "Intertidal"
                sc[1] = "2"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subsystem".format((longClassification.get() + " | " + "[" + userSubsystem + "]"), userSubsystem, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userSystem == "Riverine":

            if userSubsystem == "Tidal":
                lc[1] = "Tidal"
                sc[1] = "1"
                displayClassifications(lc, sc)

            elif userSubsystem == "Lower Perennial":
                lc[1] = "Lower Perennial"
                sc[1] = "2"
                displayClassifications(lc, sc)

            elif userSubsystem == "Upper Perennial":
                lc[1] = "Upper Perennial"
                sc[1] = "3"
                displayClassifications(lc, sc)

            elif userSubsystem == "Intermittent":
                lc[1] = "Intermittent"
                sc[1] = "4"
                displayClassifications(lc, sc)

            elif userSubsystem == "Unknown Perennial":
                lc[1] = "Unknown Perennial"
                sc[1] = "5"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subsystem".format((longClassification.get() + " | " + "[" + userSubsystem + "]"), userSubsystem, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

            # All riverine subsystems share the same class list
            dictClass = ['Rock Bottom', 'Unconsolidated Bottom', 'Streambed', 'Aquatic Bed', 'Rocky Shore', 'Unconsolidated Shore', 'Emergent']

            for choice in dictClass:
                cboxClass['menu'].add_command(label = choice,
                    command = tk._setit(svClass, choice))

        elif userSystem == "Lacustrine":

            if userSubsystem == "Limnetic":
                dictClass = ['Rock Bottom', 'Unconsolidated Bottom', 'Aquatic Bed']
                for choice in dictClass:
                    cboxClass['menu'].add_command(label = choice,
                        command = tk._setit(svClass, choice))

                lc[1] = "Limnetic"
                sc[1] = "1"
                displayClassifications(lc, sc)

            elif userSubsystem == "Littoral":
                dictClass = ['Rock Bottom', 'Unconsolidated Bottom', 'Aquatic Bed', 'Rocky Shore', 'Unconsolidated Shore', 'Emergent']
                for choice in dictClass:
                    cboxClass['menu'].add_command(label = choice,
                        command = tk._setit(svClass, choice))

                lc[1] = "Littoral"
                sc[1] = "2"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subsystem".format((longClassification.get() + " | " + "[" + userSubsystem + "]"), userSubsystem, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userSystem == "Palustrine":
            dictClass = ['Rock Bottom', 'Unconsolidated Bottom', 'Aquatic Bed', 'Unconsolidated Shore', 'Moss-Lichen', 'Emergent', 'Scrub-Shrub', 'Forested']
            for choice in dictClass:
                cboxClass['menu'].add_command(label = choice,
                    command = tk._setit(svClass, choice))

            lc[1] = "Not Applicable"
            sc[1] = "N/A"
            displayClassifications(lc, sc)

        elif userSystem == "Upland":

            if userSubsystem == "Urban":
                dictClass = ['High Intensity (Industrial)', 'Moderate Intensity', 'Low Intensity (Residential)', 'Developed Open Space']
                for choice in dictClass:
                    cboxClass['menu'].add_command(label = choice,
                        command = tk._setit(svClass, choice))

                lc[1] = "Urban"
                sc[1] = "U"
                displayClassifications(lc, sc)

            elif userSubsystem == "Agriculture":
                dictClass = ['Not Applicable']
                for choice in dictClass:
                    cboxClass['menu'].add_command(label = choice,
                        command = tk._setit(svClass, choice))

                lc[1] = "Agriculture"
                sc[1] = "A"
                displayClassifications(lc, sc)

            elif userSubsystem == "Range":
                dictClass = ['Not Applicable']
                for choice in dictClass:
                    cboxClass['menu'].add_command(label = choice,
                        command = tk._setit(svClass, choice))

                lc[1] = "Range"
                sc[1] = "R"
                displayClassifications(lc, sc)

            elif userSubsystem == "Forest":
                dictClass = ['Deciduous', 'Evergreen', 'Mixed']
                for choice in dictClass:
                    cboxClass['menu'].add_command(label = choice,
                        command = tk._setit(svClass, choice))

                lc[1] = "Forest"
                sc[1] = "F"
                displayClassifications(lc, sc)

            elif userSubsystem == "Barren":
                dictClass = ['Not Applicable']
                for choice in dictClass:
                    cboxClass['menu'].add_command(label = choice,
                        command = tk._setit(svClass, choice))

                lc[1] = "Barren"
                sc[1] = "B"
                displayClassifications(lc, sc)

            elif userSubsystem == "Scrub/Shrub":
                dictClass = ['Deciduous', 'Evergreen', 'Mixed']
                for choice in dictClass:
                    cboxClass['menu'].add_command(label = choice,
                        command = tk._setit(svClass, choice))

                lc[1] = "Scrub/Shrub"
                sc[1] = "SS"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subsystem".format((longClassification.get() + " | " + "[" + userSubsystem + "]"), userSubsystem, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        else:
            frameinfo = getframeinfo(currentframe())
            errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a System | [1]".format((longClassification.get() + " | " + "[" + userSystem + "]"), userSystem, frameinfo.lineno)
            arcpy.AddMessage(errorMessage)
            errorLog.append(errorMessage)


def eClass(*args):

    global cboxClass
    global cboxSubclass
    global cboxModifiers

    global dictClass
    global dictSubclass
    global dictModifiers

    global lc
    global sc

    if len(dictSubclass) > 0:

        # Clear all lower echelon comboboxes/selections
        # Reset selections
        svSubclass.set('')
        svModifiers.set('')

        # Reset global tracking variables
        dictSubclass = []
        dictModifiers = []

        # Delete lists
        cboxSubclass['menu'].delete(0, 'end')
        cboxModifiers['menu'].delete(0, 'end')

        # Clean up Short & Long Classifications
        for i in range(2, len(lc)):
            lc[i] = "N/A"
        for i in range(2, len(sc)):
            sc[i] = "N/A"

    # Build new selections
    userSystem = svSystem.get()
    userSubsystem = svSubsystem.get()
    userClass = svClass.get()

    if (len(userSystem) > 1
        and len(userSubsystem) > 1
        and len(userClass) > 1):

        if userSystem == "Marine":

            if userSubsystem == "Subtidal":

                if userClass == "Rock Bottom":

                    dictSubclass = ['Bedrock', 'Rubble', 'Not Applicable']

                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Rock Bottom"
                    sc[2] = "RB"

                    displayClassifications(lc, sc)

                elif userClass == "Unconsolidated Bottom":

                    dictSubclass = ['Cobble-Gravel', 'Sand', 'Mud', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Unconsolidated Bottom"
                    sc[2] = "UB"
                    displayClassifications(lc, sc)

                elif userClass == "Aquatic Bed":

                    dictSubclass = ['Algal', 'Rooted Vascular', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Aquatic Bed"
                    sc[2] = "AB"
                    displayClassifications(lc, sc)

                elif userClass == "Reef":

                    dictSubclass = ['Coral', 'Worm', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Reef"
                    sc[2] = "RF"
                    displayClassifications(lc, sc)

                else:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Class".format((longClassification.get() + " | " + "[" + userClass + "]"), userClass, frameinfo.lineno)
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)

            elif userSubsystem == "Intertidal":

                if userClass == "Aquatic Bed":

                    dictSubclass = ['Algal', 'Rooted Vascular', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Aquatic Bed"
                    sc[2] = "AB"
                    displayClassifications(lc, sc)

                elif userClass == "Reef":

                    dictSubclass = ['Coral', 'Worm', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Reef"
                    sc[2] = "RF"
                    displayClassifications(lc, sc)

                elif userClass == "Rocky Shore":

                    dictSubclass = ['Bedrock', 'Rubble', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Rock Shore"
                    sc[2] = "RS"
                    displayClassifications(lc, sc)

                elif userClass == "Unconsolidated Shore":

                    dictSubclass = ['Cobble-Gravel', 'Sand', 'Mud', 'Organic', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Unconsolidated Shore"
                    sc[2] = "US"
                    displayClassifications(lc, sc)

                else:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Class".format((longClassification.get() + " | " + "[" + userClass + "]"), userClass, frameinfo.lineno)
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subsystem".format((longClassification.get() + " | " + "[" + userSubsystem + "]"), userSubsystem, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userSystem == "Estuarine":

            if userSubsystem == "Subtidal":

                if userClass == "Rock Bottom":

                    dictSubclass = ['Bedrock', 'Rubble', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Rock Bottom"
                    sc[2] = "RB"
                    displayClassifications(lc, sc)

                elif userClass == "Unconsolidated Bottom":

                    dictSubclass = ['Cobble-Gravel', 'Sand', 'Mud', 'Organic', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Unconsolidated Bottom"
                    sc[2] = "UB"
                    displayClassifications(lc, sc)

                elif userClass == "Aquatic Bed":

                    dictSubclass = ['Algal', 'Rooted Vascular', 'Floating Vascular', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Aquatic Bed"
                    sc[2] = "AB"
                    displayClassifications(lc, sc)

                elif userClass == "Reef":

                    dictSubclass = ['Mollusk', 'Worm', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Reef"
                    sc[2] = "RF"
                    displayClassifications(lc, sc)

                else:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Class".format((longClassification.get() + " | " + "[" + userClass + "]"), userClass, frameinfo.lineno)
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)

            elif userSubsystem == "Intertidal":

                if userClass == "Aquatic Bed":

                    dictSubclass = ['Algal', 'Rooted Vascular', 'Floating Vascular', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Aquatic Bed"
                    sc[2] = "AB"
                    displayClassifications(lc, sc)

                elif userClass == "Reef":

                    dictSubclass = ['Mollusk', 'Worm', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Reef"
                    sc[2] = "RF"
                    displayClassifications(lc, sc)

                elif userClass == "Streambed":

                    dictSubclass = ['Bedrock', 'Rubble', 'Cobbel-Gravel', 'Sand', 'Mud', 'Organic', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Streambed"
                    sc[2] = "SB"
                    displayClassifications(lc, sc)

                elif userClass == "Rocky Shore":

                    dictSubclass = ['Bedrock', 'Rubble', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Rock Shore"
                    sc[2] = "RS"
                    displayClassifications(lc, sc)

                elif userClass == "Unconsolidated Shore":

                    dictSubclass = ['Cobble-Gravel', 'Sand', 'Mud', 'Organic', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Unconsolidated Shore"
                    sc[2] = "US"
                    displayClassifications(lc, sc)

                elif userClass == "Emergent":

                    dictSubclass = ['Persistent', 'Nonpersistent', 'Phragmites australis', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Emergent"
                    sc[2] = "EM"
                    displayClassifications(lc, sc)

                elif userClass == "Scrub-Shrub":

                    dictSubclass = ['Broad-Leaved Deciduous', 'Needle-Leaved Deciduous', 'Broad-Leaved Evergreen', 'Needle-Leaved Evergreen', 'Dead', 'Deciduous', 'Evergreen', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Scrub Shrub"
                    sc[2] = "SS"
                    displayClassifications(lc, sc)

                elif userClass == "Forested":

                    dictSubclass = ['Broad-Leaved Deciduous', 'Needle-Leaved Deciduous', 'Broad-Leaved Evergreen', 'Needle-Leaved Evergreen', 'Dead', 'Deciduous', 'Evergreen', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Forested"
                    sc[2] = "FO"
                    displayClassifications(lc, sc)

                else:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Class".format((longClassification.get() + " | " + "[" + userClass + "]"), userClass, frameinfo.lineno)
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subsystem".format((longClassification.get() + " | " + "[" + userSubsystem + "]"), userSubsystem, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userSystem == "Riverine":

            # Skip consideration of userSubsystem

            if userClass == "Rock Bottom":

                dictSubclass = ['Bedrock', 'Rubble', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Rock Bottom"
                sc[2] = "RB"
                displayClassifications(lc, sc)

            elif userClass == "Unconsolidated Bottom":

                dictSubclass = ['Cobble-Gravel', 'Sand', 'Mud', 'Organic', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Unconsolidated Bottom"
                sc[2] = "UB"
                displayClassifications(lc, sc)

            elif userClass == "Streambed":

                dictSubclass = ['Bedrock', 'Rubble', 'Cobbel-Gravel', 'Sand', 'Mud', 'Organic', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Streambed"
                sc[2] = "SB"
                displayClassifications(lc, sc)

            elif userClass == "Aquatic Bed":

                dictSubclass = ['Algal', 'Rooted Vascular', 'Floating Vascular', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Aquatic Bed"
                sc[2] = "AB"
                displayClassifications(lc, sc)

            elif userClass == "Rocky Shore":

                dictSubclass = ['Bedrock', 'Rubble', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Rock Shore"
                sc[2] = "RS"
                displayClassifications(lc, sc)

            elif userClass == "Unconsolidated Shore":

                dictSubclass = ['Cobble-Gravel', 'Sand', 'Mud', 'Organic', 'Vegetated', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Unconsolidated Shore"
                sc[2] = "US"
                displayClassifications(lc, sc)

            elif userClass == "Emergent":

                dictSubclass = ['Nonpersistent', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Emergent"
                sc[2] = "EM"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Class".format((longClassification.get() + " | " + "[" + userClass + "]"), userClass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userSystem == "Lacustrine":

            if userSubsystem == "Limnetic":

                if userClass == "Rock Bottom":

                    dictSubclass = ['Bedrock', 'Rubble', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Rock Bottom"
                    sc[2] = "RB"
                    displayClassifications(lc, sc)

                elif userClass == "Unconsolidated Bottom":

                    dictSubclass = ['Cobble-Gravel', 'Sand', 'Mud', 'Organic', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Unconsolidated Bottom"
                    sc[2] = "UB"
                    displayClassifications(lc, sc)

                elif userClass == "Aquatic Bed":

                    dictSubclass = ['Algal', 'Aquatic Moss', 'Rooted Vascular', 'Floating Vascular', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Aquatic Bed"
                    sc[2] = "AB"
                    displayClassifications(lc, sc)

                else:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Class".format((longClassification.get() + " | " + "[" + userClass + "]"), userClass, frameinfo.lineno)
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)

            elif userSubsystem == "Littoral":

                if userClass == "Rock Bottom":

                    if userClass == "Rock Bottom":

                        dictSubclass = ['Bedrock', 'Rubble', 'Not Applicable']
                        for choice in dictSubclass:
                            cboxSubclass['menu'].add_command(label = choice,
                                command = tk._setit(svSubclass, choice))

                        lc[2] = "Rock Bottom"
                        sc[2] = "RB"
                        displayClassifications(lc, sc)

                elif userClass == "Unconsolidated Bottom":

                    dictSubclass = ['Cobble-Gravel', 'Sand', 'Mud', 'Organic', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Unconsolidated Bottom"
                    sc[2] = "UB"
                    displayClassifications(lc, sc)

                elif userClass == "Aquatic Bed":

                    dictSubclass = ['Algal', 'Aquatic Moss', 'Rooted Vascular', 'Floating Vascular', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Aquatic Bed"
                    sc[2] = "AB"
                    displayClassifications(lc, sc)

                elif userClass == "Rocky Shore":

                    dictSubclass = ['Bedrock', 'Rubble', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Rock Shore"
                    sc[2] = "RS"
                    displayClassifications(lc, sc)

                elif userClass == "Unconsolidated Shore":

                    dictSubclass = ['Cobble-Gravel', 'Sand', 'Mud', 'Organic', 'Vegetated', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Unconsolidated Shore"
                    sc[2] = "US"
                    displayClassifications(lc, sc)

                elif userClass == "Emergent":

                    dictSubclass = ['Nonpersistent', 'Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Emergent"
                    sc[2] = "EM"
                    displayClassifications(lc, sc)

                else:
                    frameinfo = getframeinfo(currentframe())
                    errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Class".format((longClassification.get() + " | " + "[" + userClass + "]"), userClass, frameinfo.lineno)
                    arcpy.AddMessage(errorMessage)
                    errorLog.append(errorMessage)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subsystem".format((longClassification.get() + " | " + "[" + userSubsystem + "]"), userSubsystem, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userSystem == "Palustrine":

            if userClass == "Rock Bottom":

                dictSubclass = ['Bedrock', 'Rubble', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Rock Bottom"
                sc[2] = "RB"
                displayClassifications(lc, sc)

            elif userClass == "Unconsolidated Bottom":

                dictSubclass = ['Cobble-Gravel', 'Sand', 'Mud', 'Organic', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Unconsolidated Bottom"
                sc[2] = "UB"
                displayClassifications(lc, sc)

            elif userClass == "Aquatic Bed":

                dictSubclass = ['Algal', 'Aquatic Moss', 'Rooted Vascular', 'Floating Vascular', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Aquatic Bed"
                sc[2] = "AB"
                displayClassifications(lc, sc)

            elif userClass == "Unconsolidated Shore":

                dictSubclass = ['Cobble-Gravel', 'Sand', 'Mud', 'Organic', 'Vegetated', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Unconsolidated Shore"
                sc[2] = "US"
                displayClassifications(lc, sc)

            elif userClass == "Moss-Lichen":

                dictSubclass = ['Moss', 'Lichen', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Moss-Lichen"
                sc[2] = "ML"
                displayClassifications(lc, sc)

            elif userClass == "Emergent":

                dictSubclass = ['Persistent', 'Nonpersistent', 'Phragmites australis', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Emergent"
                sc[2] = "EM"
                displayClassifications(lc, sc)

            elif userClass == "Scrub-Shrub":

                dictSubclass = ['Broad-Leaved Deciduous', 'Needle-Leaved Deciduous', 'Broad-Leaved Evergreen', 'Needle-Leaved Evergreen', 'Dead', 'Deciduous', 'Evergreen', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Scrub Shrub"
                sc[2] = "SS"
                displayClassifications(lc, sc)

            elif userClass == "Forested":

                dictSubclass = ['Broad-Leaved Deciduous', 'Needle-Leaved Deciduous', 'Broad-Leaved Evergreen', 'Needle-Leaved Evergreen', 'Dead', 'Deciduous', 'Evergreen', 'Not Applicable']
                for choice in dictSubclass:
                    cboxSubclass['menu'].add_command(label = choice,
                        command = tk._setit(svSubclass, choice))

                lc[2] = "Forested"
                sc[2] = "FO"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Class".format((longClassification.get() + " | " + "[" + userClass + "]"), userClass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userSystem == "Upland":

            if userSubsystem == "Urban":

                if userClass == "High Intensity (Industrial)":

                    dictSubclass = ['Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "High Intensity (Industrial)"
                    sc[2] = "1"
                    displayClassifications(lc, sc)

                elif userClass == "Moderate Intensity":

                    dictSubclass = ['Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Moderate Intensity"
                    sc[2] = "2"
                    displayClassifications(lc, sc)

                elif userClass == "Low Intensity (Residential)":

                    dictSubclass = ['Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Low Intensity (Residential)"
                    sc[2] = "3"
                    displayClassifications(lc, sc)

                elif userClass == "Developed Open Space":

                    dictSubclass = ['Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Developed Open Space"
                    sc[2] = "4"
                    displayClassifications(lc, sc)

            elif ((userSubsystem == "Range") or (userSubsystem == "Agriculture") or (userSubsystem == "Barren")):

                if userClass == "Not Applicable":

                    dictSubclass = ['Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Not Applicable"
                    sc[2] = "N/A"
                    displayClassifications(lc, sc)

            elif userSubsystem == "Forest" or userSubsystem == "Scrub/Shrub":

                if userClass == "Deciduous":

                    dictSubclass = ['Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Deciduous"
                    sc[2] = "6"
                    displayClassifications(lc, sc)

                elif userClass == "Evergreen":

                    dictSubclass = ['Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Evergreen"
                    sc[2] = "7"
                    displayClassifications(lc, sc)

                elif userClass == "Mixed":

                    dictSubclass = ['Not Applicable']
                    for choice in dictSubclass:
                        cboxSubclass['menu'].add_command(label = choice,
                            command = tk._setit(svSubclass, choice))

                    lc[2] = "Mixed"
                    sc[2] = "8"
                    displayClassifications(lc, sc)


            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Class".format((longClassification.get() + " | " + "[" + userClass + "]"), userClass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        else:
            frameinfo = getframeinfo(currentframe())
            errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a System | [1]".format((longClassification.get() + " | " + "[" + userSystem + "]"), userSystem, frameinfo.lineno)
            arcpy.AddMessage(errorMessage)
            errorLog.append(errorMessage)


def eSubclass(*args):

    global cboxSubclass
    global cboxModifiers

    global dictSubclass
    global dictModifiers

    global lc
    global sc

    if len(dictModifiers) > 0:


        # Clear all lower echelon comboboxes/selections
        # Reset selections
        svModifiers.set('')

        # Reset global tracking variables
        dictModifiers = []

        # Delete lists
        cboxModifiers['menu'].delete(0, 'end')

        # Clean up Short & Long Classifications
        lc[3] = "N/A"
        sc[3] = "N/A"
        lc[4] = "N/A"
        sc[4] = "N/A"

    # Build new selections
    userClass = svClass.get()
    userSubclass = svSubclass.get()

    if (len(userClass) > 1 and len(userSubclass) > 1):

        if userClass == "Rock Bottom":

            if userSubclass == "Bedrock":
                lc[3] = "Bedrock"
                sc[3] = "1"
                displayClassifications(lc, sc)

            elif userSubclass == "Rubble":
                lc[3] = "Rubble"
                sc[3] = "2"
                displayClassifications(lc, sc)

            elif userSubclass == "Not Applicable":
                lc[3] = "Not Applicable"
                sc[3] = "N/A"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subclass | [1]".format( (longClassification.get() + " | " + "[" + userSubclass + "]") , userSubclass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)
                arcpy.AddMessage(errorLog)

        elif userClass == "Unconsolidated Bottom":

            if userSubclass == "Cobble-Gravel":
                lc[3] = "Cobble-Gravel"
                sc[3] = "1"
                displayClassifications(lc, sc)

            elif userSubclass == "Sand":
                lc[3] = "Sand"
                sc[3] = "2"
                displayClassifications(lc, sc)

            elif userSubclass == "Mud":
                lc[3] = "Mud"
                sc[3] = "3"
                displayClassifications(lc, sc)

            elif userSubclass == "Organic":
                lc[3] = "Organic"
                sc[3] = "4"
                displayClassifications(lc, sc)

            elif userSubclass == "Not Applicable":
                lc[3] = "Not Applicable"
                sc[3] = "N/A"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subclass | [1]".format((longClassification.get() + " | " + "[" + userSubclass + "]"), userSubclass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userClass == "Aquatic Bed":

            if userSubclass == "Algal":
                lc[3] = "Algal"
                sc[3] = "1"
                displayClassifications(lc, sc)

            elif userSubclass == "Aquatic Moss":
                lc[3] = "Aquatic Moss"
                sc[3] = "2"
                displayClassifications(lc, sc)

            elif userSubclass == "Rooted Vascular":
                lc[3] = "Rooted Vascular"
                sc[3] = "3"
                displayClassifications(lc, sc)

            elif userSubclass == "Floating Vascular":
                lc[3] = "Floating Vascular"
                sc[3] = "4"
                displayClassifications(lc, sc)

            elif userSubclass == "Not Applicable":
                lc[3] = "Not Applicable"
                sc[3] = "N/A"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subclass | [1]".format((longClassification.get() + " | " + "[" + userSubclass + "]"), userSubclass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userClass == "Reef":

            if userSubclass == "Coral":
                lc[3] = "Coral"
                sc[3] = "1"
                displayClassifications(lc, sc)

            elif userSubclass == "Mollusk":
                lc[3] = "Mollusk"
                sc[3] = "2"
                displayClassifications(lc, sc)

            elif userSubclass == "Worm":
                lc[3] = "Worm"
                sc[3] = "3"
                displayClassifications(lc, sc)
                displayClassifications(lc, sc)

            elif userSubclass == "Not Applicable":
                lc[3] = "Not Applicable"
                sc[3] = "N/A"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subclass | [1]".format((longClassification.get() + " | " + "[" + userSubclass + "]"), userSubclass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userClass == "Rocky Shore":

            if userSubclass == "Bedrock":
                lc[3] = "Bedrock"
                sc[3] = "1"
                displayClassifications(lc, sc)

            elif userSubclass == "Rubble":
                lc[3] = "Rubble"
                sc[3] = "2"
                displayClassifications(lc, sc)

            elif userSubclass == "Not Applicable":
                lc[3] = "Not Applicable"
                sc[3] = "N/A"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subclass | [1]".format((longClassification.get() + " | " + "[" + userSubclass + "]"), userSubclass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userClass == "Unconsolidated Shore":

            if userSubclass == "Cobble-Gravel":
                lc[3] = "Cobble-Gravel"
                sc[3] = "1"
                displayClassifications(lc, sc)

            elif userSubclass == "Sand":
                lc[3] = "Sand"
                sc[3] = "2"
                displayClassifications(lc, sc)

            elif userSubclass == "Mud":
                lc[3] = "Mud"
                sc[3] = "3"
                displayClassifications(lc, sc)

            elif userSubclass == "Organic":
                lc[3] = "Organic"
                sc[3] = "4"
                displayClassifications(lc, sc)

            elif userSubclass == "Vegetated":
                lc[3] = "Vegetated"
                sc[3] = "5"
                displayClassifications(lc, sc)

            elif userSubclass == "Not Applicable":
                lc[3] = "Not Applicable"
                sc[3] = "N/A"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subclass | [1]".format((longClassification.get() + " | " + "[" + userSubclass + "]"), userSubclass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userClass == "Streambed":

            if userSubclass == "Bedrock":
                lc[3] = "Bedrock"
                sc[3] = "1"
                displayClassifications(lc, sc)

            elif userSubclass == "Rubble":
                lc[3] = "Rubble"
                sc[3] = "2"
                displayClassifications(lc, sc)

            elif userSubclass == "Cobbel-Gravel":
                lc[3] = "Cobbel-Gravel"
                sc[3] = "3"
                displayClassifications(lc, sc)

            elif userSubclass == "Sand":
                lc[3] = "Sand"
                sc[3] = "4"
                displayClassifications(lc, sc)

            elif userSubclass == "Mud":
                lc[3] = "Mud"
                sc[3] = "5"
                displayClassifications(lc, sc)

            elif userSubclass == "Organic":
                lc[3] = "Organic"
                sc[3] = "6"
                displayClassifications(lc, sc)

            elif userSubclass == "Not Applicable":
                lc[3] = "Not Applicable"
                sc[3] = "N/A"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subclass | [1]".format((longClassification.get() + " | " + "[" + userSubclass + "]"), userSubclass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userClass == "Emergent":

            if userSubclass == "Persistent":
                lc[3] = "Persistent"
                sc[3] = "1"
                displayClassifications(lc, sc)

            elif userSubclass == "Nonpersistent":
                lc[3] = "Nonpersistent"
                sc[3] = "2"
                displayClassifications(lc, sc)

            elif userSubclass == "Phragmites australis":
                lc[3] = "Phragmites australis"
                sc[3] = "5"
                displayClassifications(lc, sc)

            elif userSubclass == "Not Applicable":
                lc[3] = "Not Applicable"
                sc[3] = "N/A"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subclass | [1]".format((longClassification.get() + " | " + "[" + userSubclass + "]"), userSubclass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userClass == "Scrub-Shrub":

            if userSubclass == "Broad-Leaved Deciduous":
                lc[3] = "Broad-Leaved Deciduous"
                sc[3] = "1"
                displayClassifications(lc, sc)

            elif userSubclass == "Needle-Leaved Deciduous":
                lc[3] = "Needle-Leaved Deciduous"
                sc[3] = "2"
                displayClassifications(lc, sc)

            elif userSubclass == "Broad-Leaved Evergreen":
                lc[3] = "Broad-Leaved Evergreen"
                sc[3] = "3"
                displayClassifications(lc, sc)

            elif userSubclass == "Needle-Leaved Evergreen":
                lc[3] = "Needle-Leaved Evergreen"
                sc[3] = "4"
                displayClassifications(lc, sc)

            elif userSubclass == "Dead":
                lc[3] = "Dead"
                sc[3] = "5"
                displayClassifications(lc, sc)

            elif userSubclass == "Deciduous":
                lc[3] = "Deciduous"
                sc[3] = "6"
                displayClassifications(lc, sc)

            elif userSubclass == "Evergreen":
                lc[3] = "Evergreen"
                sc[3] = "7"
                displayClassifications(lc, sc)

            elif userSubclass == "Not Applicable":
                lc[3] = "Not Applicable"
                sc[3] = "N/A"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subclass | [1]".format((longClassification.get() + " | " + "[" + userSubclass + "]"), userSubclass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userClass == "Forested":

            if userSubclass == "Broad-Leaved Deciduous":
                lc[3] = "Broad-Leaved Deciduous"
                sc[3] = "1"
                displayClassifications(lc, sc)

            elif userSubclass == "Needle-Leaved Deciduous":
                lc[3] = "Needle-Leaved Deciduous"
                sc[3] = "2"
                displayClassifications(lc, sc)

            elif userSubclass == "Broad-Leaved Evergreen":
                lc[3] = "Broad-Leaved Evergreen"
                sc[3] = "3"
                displayClassifications(lc, sc)

            elif userSubclass == "Needle-Leaved Evergreen":
                lc[3] = "Needle-Leaved Evergreen"
                sc[3] = "4"
                displayClassifications(lc, sc)

            elif userSubclass == "Dead":
                lc[3] = "Dead"
                sc[3] = "5"
                displayClassifications(lc, sc)

            elif userSubclass == "Deciduous":
                lc[3] = "Deciduous"
                sc[3] = "6"
                displayClassifications(lc, sc)

            elif userSubclass == "Evergreen":
                lc[3] = "Evergreen"
                sc[3] = "7"
                displayClassifications(lc, sc)

            elif userSubclass == "Not Applicable":
                lc[3] = "Not Applicable"
                sc[3] = "N/A"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subclass | [1]".format((longClassification.get() + " | " + "[" + userSubclass + "]"), userSubclass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif userClass == "Moss-Lichen":

            if userSubclass == "Moss":
                lc[3] = "Moss"
                sc[3] = "1"
                displayClassifications(lc, sc)

            elif userSubclass == "Lichen":
                lc[3] = "Lichen"
                sc[3] = "2"
                displayClassifications(lc, sc)

            elif userSubclass == "Not Applicable":
                lc[3] = "Not Applicable"
                sc[3] = "N/A"
                displayClassifications(lc, sc)

            else:
                frameinfo = getframeinfo(currentframe())
                errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Subclass | [1]".format((longClassification.get() + " | " + "[" + userSubclass + "]"), userSubclass, frameinfo.lineno)
                arcpy.AddMessage(errorMessage)
                errorLog.append(errorMessage)

        elif (userClass == 'High Intensity (Industrial)') or (userClass == 'Moderate Intensity') or (userClass == 'Low Intensity (Residential)') or (userClass == 'Developed Open Space') or (userClass == 'Not Applicable') or (userClass == 'Deciduous') or (userClass == 'Evergreen') or (userClass == 'Mixed'):
            lc[3] = "Not Applicable"
            sc[3] = "N/A"
            displayClassifications(lc, sc)

        else:
            frameinfo = getframeinfo(currentframe())
            errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Class | [1]".format((longClassification.get() + " | " + "[" + userClass + "]"), userClass, frameinfo.lineno)
            arcpy.AddMessage(errorMessage)
            errorLog.append(errorMessage)

    dictModifiers = ['Temporarily Flooded',
    'Saturated',
    'Seasonally Flooded',
    'Seasonally Flooded/Saturated',
    'Semipermanently Flooded',
    'Intermittently Exposed',
    'Permanently Flooded',
    'Intermittently Flooded',
    'Artificially Flooded',
    'Subtidal',
    'Irregularly Exposed',
    'Regularly Exposed',
    'Irregularly Flooded',
    'Temporarily Flooded-Tidal',
    'Seasonally Flooded-Tidal',
    'Semipermanently Flooded-Tidal',
    'Permanently Flooded-Tidal',
    'Beaver',
    'Partly Drained/Ditched',
    'Farmed',
    'Diked/Impounded',
    'Artificial',
    'Spoil',
    'Excavated',
    'Hyperhaline',
    'Euhaline',
    'Mixohaline (Brackish)',
    'Polyhaline',
    'Mesohaline',
    'Oligohaline',
    'Fresh',
    'Hypersaline',
    'Eusaline',
    'Mixosaline',
    'Acid',
    'Circumneutral',
    'Alkaline',
    'Organic',
    'Mineral']

    for choice in dictModifiers:
        cboxModifiers['menu'].add_command(label = choice,
            command = tk._setit(svModifiers, choice))


def eModifiers(*args):

    global cboxModifiers

    global dictModifiers

    global lc
    global sc

    userSubclass = svSubclass.get()
    userModifiers = svModifiers.get()

    if len(userSubclass) > 1 and len(userModifiers) > 1:
        if userModifiers == 'Temporarily Flooded':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'A'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'A'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Saturated':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'B'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'B'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Seasonally Flooded':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'C'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'C'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Seasonally Flooded/Saturated':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'E'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'E'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Semipermanently Flooded':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'F'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'F'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Intermittently Exposed':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'G'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'G'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Permanently Flooded':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'H'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'H'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Intermittently Flooded':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'J'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'J'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Artificially Flooded':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'K'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'K'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Subtidal':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'L'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'L'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Irregularly Exposed':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'M'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'M'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Regularly Exposed':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'N'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'N'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Irregularly Flooded':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'P'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'P'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Temporarily Flooded-Tidal':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'S'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'S'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Seasonally Flooded-Tidal':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'R'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'R'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Semipermanently Flooded-Tidal':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'T'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'T'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Permanently Flooded-Tidal':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'V'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'V'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Beaver':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'b'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'b'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Partly Drained/Ditched':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'd'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'd'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Farmed':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'f'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'f'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Diked/Impounded':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'h'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'h'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Artificial':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'r'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'r'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Spoil':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 's'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 's'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Excavated':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'x'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'x'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Hyperhaline':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = '1'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], '1'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Euhaline':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = '2'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], '2'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Mixohaline (Brackish)':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = '3'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], '3'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Polyhaline':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = '4'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], '4'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Mesohaline':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = '5'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], '5'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Oligohaline':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = '6'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], '6'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Fresh':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = '0'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], '0'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Hypersaline':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = '7'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], '7'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Eusaline':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = '8'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], '8'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Mixosaline':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = '9'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], '9'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Acid':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'a'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'a'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Circumneutral':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 't'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 't'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Alkaline':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'l'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'l'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Organic':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'g'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'g'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        elif userModifiers == 'Mineral':
            if lc[4] == "N/A":
                lc[4] = userModifiers
                sc[4] = 'm'
            else:
                if userModifiers not in lc[4]:
                    lctemp = ", ".join([lc[4], userModifiers])
                    sctemp = "".join([sc[4], 'm'])
                    lc[4] = lctemp
                    sc[4] = sctemp
            displayClassifications(lc, sc)
        else:
            frameinfo = getframeinfo(currentframe())
            errorMessage = "[!][line {2}] {0} is an invalid classification. {1} is not a Modifier".format((longClassification.get() + " | " + "[" + userModifiers + "]"), userModifiers, frameinfo.lineno)
            arcpy.AddMessage(errorMessage)
            errorLog.append(errorMessage)



# Get selection from ArcMap ----------------------------------------------------
try:
    currentMap = arcpy.mapping.MapDocument("CURRENT")
    dataFrame = arcpy.mapping.ListDataFrames(currentMap)[0]
    currentLayer = arcpy.mapping.ListLayers(dataFrame, '', None)[0]
except Exception as e:
    arcpy.AddMessage(e)


# GUI Application --------------------------------------------------------------
root = tk.Tk()
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)
root.wm_title("Edit Data Frame")

masterFrame = ttk.Frame(root, width = 400, height = 600)
masterFrame.grid(column = 0, row = 0)
masterFrame.columnconfigure(0, weight = 1)
masterFrame.rowconfigure(0, weight = 1)

# Build "Close Warning" frame
closeFrame = ttk.Frame(masterFrame)
closeFrame.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)
closeFrame.columnconfigure(0, weight = 1)
closeFrame.rowconfigure(0, weight = 1)

# Build & place "Close Warning" label
closeWarning = ttk.Label(closeFrame,
    text = "Exit this window first", foreground = "red")
closeWarning.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)

# Build content Frame
contentFrame = ttk.Frame(masterFrame)
contentFrame.grid(column = 0, row = 1, columnspan = 2, padx = 5, pady = 5)
contentFrame.columnconfigure(0, weight = 1)
contentFrame.rowconfigure(0, weight = 1)

# To be filled by the user's selection
longClassification = tk.StringVar(root)
shortClassification = tk.StringVar(root)

# [0] System, [1] Subsystem, [2] Class, [3] Subclass, [4] Modifiers
lc = ["N/A", "N/A", "N/A", "N/A", "N/A"]
sc = ["N/A", "N/A", "N/A", "N/A", "N/A"]

# Choices to fill the comboboxes/selectors
# Note: tkinter.OptionMenu requires that the first entry be blank
dictSystem = ["", "Lacustrine", "Palustrine", "Marine", "Estuarine", "Riverine", "Upland"]
dictSubsystem = []
dictClass = []
dictSubclass = []
dictModifiers = []

# Labels for the comboboxes/selectors
labelSystem = ttk.Label(contentFrame, text = "System")
labelSubsystem = ttk.Label(contentFrame, text = "Subsystem")
labelClass = ttk.Label(contentFrame, text = "Class")
labelSubclass = ttk.Label(contentFrame, text = "Subclass")
labelModifiers = ttk.Label(contentFrame, text = "Modifiers")

# Build comboboxes/selectors
svSystem = tk.StringVar(root)
svSubsystem = tk.StringVar(root)
svClass = tk.StringVar(root)
svSubclass = tk.StringVar(root)
svModifiers = tk.StringVar(root)
ivErrorBox = tk.IntVar(root)
ivNullBox = tk.IntVar(root)
ivModBox = tk.IntVar(root)

svSystem.trace("w", eSystem)
svSubsystem.trace("w", eSubsystem)
svClass.trace("w", eClass)
svSubclass.trace("w", eSubclass)
svModifiers.trace("w", eModifiers)

cboxSystem = ttk.OptionMenu(contentFrame, svSystem, *dictSystem)
cboxSubsystem = ttk.OptionMenu(contentFrame, svSubsystem, *dictSubsystem)
cboxClass = ttk.OptionMenu(contentFrame, svClass, *dictClass)
cboxSubclass = ttk.OptionMenu(contentFrame, svSubclass, *dictSubclass)
cboxModifiers = ttk.OptionMenu(contentFrame, svModifiers, *dictModifiers)

# Place labels and comboboxes/selectors
labelSystem.grid(row = 1, column = 1, padx=5, pady=5)
cboxSystem.grid(row =1, column = 2, padx=5, pady=5)

labelSubsystem.grid(row = 2, column = 1, padx=5, pady=5)
cboxSubsystem.grid(row = 2, column = 2, padx=5, pady=5)

labelClass.grid(row = 3, column = 1, padx=5, pady=5)
cboxClass.grid(row = 3, column = 2, padx=5, pady=5)

labelSubclass.grid(row = 4, column = 1, padx=5, pady=5)
cboxSubclass.grid(row = 4, column = 2, padx=5, pady=5)

labelModifiers.grid(row = 5, column = 1, padx=5, pady=5)
cboxModifiers.grid(row = 5, column = 2, padx=5, pady=5)

# Build results frame
resultsFrame = ttk.Frame(masterFrame)
resultsFrame.grid(column = 0, row = 2, columnspan = 2, padx = 5, pady= 5)
resultsFrame.columnconfigure(0, weight = 1)
resultsFrame.rowconfigure(0, weight = 1)

# Labels for results view
labelSC = ttk.Label(resultsFrame, text = "Short Classification")
labelLC = ttk.Label(resultsFrame, text = "Long Classification")
resultSC = ttk.Label(resultsFrame, textvariable = shortClassification,
    foreground = "blue")
resultLC = ttk.Label(resultsFrame, textvariable = longClassification,
    foreground = "blue")

# Place results labels
labelSC.grid(row = 1, column = 1, padx = 5, pady = 2, columnspan = 2)
labelLC.grid(row = 3, column = 1, padx = 5, pady = 2, columnspan = 2)

resultSC.grid(row = 2, column = 1, padx = 5, pady = 2, columnspan = 2)
resultLC.grid(row = 4, column = 1, padx = 5, pady = 2, columnspan = 2)

# Build submit frame
submitFrame = ttk.Frame(masterFrame)
submitFrame.grid(column = 0, row = 3, columnspan = 2, padx = 5, pady= 5)
submitFrame.columnconfigure(0, weight = 1)
submitFrame.rowconfigure(0, weight = 1)

# Build & place submit button
submitButton = ttk.Button(submitFrame, text = "Submit", command = preWrite)
submitButton.grid(row = 1, column = 1, padx =5, pady = 5, columnspan = 2)

# Build Check frame
checkFrame = ttk.Frame(masterFrame)
checkFrame.grid(column = 0, row = 4, columnspan = 2, padx = 5, pady= 5)
checkFrame.columnconfigure(0, weight = 1)
checkFrame.rowconfigure(0, weight = 1)

# Build & place Check buttons
nullBox = ttk.Checkbutton(checkFrame, text = "Allow Empty Writes",
    variable = ivNullBox)
nullBox.grid(row = 1, column = 1, padx =5, pady = 5, sticky = "W")
ivNullBox.set(0)

modBox = ttk.Checkbutton(checkFrame, text = "Force Modifiers",
    variable = ivModBox)
modBox.grid(row = 2, column = 1, padx =5, pady = 5, sticky = "W")
ivModBox.set(0)

errorBox = ttk.Checkbutton(checkFrame, text = "Log Errors",
    variable = ivErrorBox)
errorBox.grid(row = 3, column = 1, padx =5, pady = 5, sticky = "W")
ivErrorBox.set(1)

root.mainloop()