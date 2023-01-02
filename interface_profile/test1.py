# Author-
# Description-

import os
import sys
import random
import adsk.core
import adsk.fusion
import adsk.cam
import traceback
import math
# import numpy as np


def run(context):
    ui = None
    try:

        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox('Hello script')

        # get active design
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        # get all components in this design
        allComps = design.allComponents

        # get the script location
        scriptDir = os.path.dirname(os.path.realpath(__file__))

        # create a single exportManager instance
        exportMgr = design.exportManager

        # num_spline_points = [10, 20, 30, 40]
        num_spline_points = [20]

        textfile = scriptDir + "/" + 'data' + '.csv'

        # all units in cm
        graphite_width = 1
        graphite_thickness = 0.3
        putty_depth = 0.04
        vol_init = graphite_thickness*graphite_width*0.9
        vol_final = graphite_thickness*graphite_width*1.1
        full_vol_init = graphite_thickness * graphite_width
        vol_inside = full_vol_init - vol_init
        total_thickness = vol_final / graphite_width
        vol_outside = (total_thickness*graphite_width) - (graphite_thickness*graphite_width)
        putty_area = vol_inside

        with open(textfile, 'w') as f:
            f.write('filename,num_point,pore_depth,area_top,area_bottom,area_added\n')

        putty_depths = [0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]

        for putty_depth in putty_depths:
            for num in num_spline_points:  # traces through num_spline_points to generate different porosities

                # for x in range(5):  # creates a certain number of designs
                numGeom = 0
                attempts = 0
                while numGeom < 6 and attempts < 100:
                    attempts += 1
                    des = app.activeProduct
                    # Get the root component of the active design.
                    rootComp = des.rootComponent
                    # Create a new sketch on the xy plane.
                    sketches = rootComp.sketches
                    xyPlane = rootComp.xYConstructionPlane
                    sketch = sketches.add(xyPlane)

                    # create left line boundary of graphite
                    left_side = adsk.core.ObjectCollection.create()
                    left_side.add(adsk.core.Point3D.create(0, 0, 0))
                    left_side.add(adsk.core.Point3D.create(0, graphite_thickness, 0))
                    sketch.sketchCurves.sketchFittedSplines.add(left_side)

                    # create right line boundary of graphite
                    right_side = adsk.core.ObjectCollection.create()
                    right_side.add(adsk.core.Point3D.create(graphite_width, 0, 0))
                    right_side.add(adsk.core.Point3D.create(graphite_width, graphite_thickness, 0))
                    sketch.sketchCurves.sketchFittedSplines.add(right_side)

                    # create middle line
                    mid_line = adsk.core.ObjectCollection.create()
                    mid_line.add(adsk.core.Point3D.create(0, graphite_thickness/2, 0))
                    mid_line.add(adsk.core.Point3D.create(graphite_width, graphite_thickness/2, 0))
                    sketch.sketchCurves.sketchFittedSplines.add(mid_line)

                    points_bottom = adsk.core.ObjectCollection.create()  # Create an object collection for the points.
                    points_top = adsk.core.ObjectCollection.create()

                    # Enter variables here. E.g. E = 50
                    startRange = 0  # Start of range to be evaluated.
                    endRange = graphite_width  # End of range to be evaluated.
                    splinePoints = num  # Number of points that splines are generated.
                    # WARMING: Using more than a few hundred points may cause your system to hang.

                    # make the spline start at origin
                    points_bottom.add(adsk.core.Point3D.create(0, 0, 0))

                    points_top.add(adsk.core.Point3D.create(0, graphite_thickness, 0))

                    # area = areaProps.area

                    i = 1
                    while i <= (splinePoints-1):
                        t = startRange + ((endRange - startRange)/splinePoints)*i
                        xCoord = t
                        yCoord_bottom = random.uniform(0, putty_depth)
                        yCoord_top = random.uniform(graphite_thickness - putty_depth, graphite_thickness)
                        zCoord = 0

                        points_bottom.add(adsk.core.Point3D.create(xCoord, yCoord_bottom, zCoord))
                        points_top.add(adsk.core.Point3D.create(xCoord, yCoord_top, zCoord))
                        i = i + 1

                    # make the splines come back to end point
                    points_bottom.add(adsk.core.Point3D.create(graphite_width, 0, 0))
                    points_top.add(adsk.core.Point3D.create(graphite_width, graphite_thickness, 0))

                    # Generates the spline curve
                    sketch.sketchCurves.sketchFittedSplines.add(points_bottom)
                    sketch.sketchCurves.sketchFittedSplines.add(points_top)

                    # Get the profile defined by the circle
                    prof = sketch.profiles.item(0)
                    prof2 = sketch.profiles.item(1)

                    # Get area properties from a profile
                    areaProps = prof.areaProperties(adsk.fusion.CalculationAccuracy.MediumCalculationAccuracy)
                    areaProps2 = prof2.areaProperties(adsk.fusion.CalculationAccuracy.MediumCalculationAccuracy)

                    # get area
                    area = areaProps.area
                    area2 = areaProps2.area
                    # print(area + area2, vol_init)
                    # numGeom += 1
                    if abs((area + area2) - vol_init) < 0.01*vol_init:
                        numGeom += 1
                    else:
                        sketch.deleteMe()
                        continue

                    # # Create an extrusion input
                    # extrudes = rootComp.features.extrudeFeatures
                    # extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                    # extInput2 = extrudes.createInput(prof2, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

                    # # Define that the extent is a distance extent of .1 cm
                    # distance = adsk.core.ValueInput.createByReal(.1)
                    # extInput.setDistanceExtent(False, distance)
                    # extInput2.setDistanceExtent(False, distance)

                    # # Create the extrusion
                    # extrudeFeature = extrudes.add(extInput)
                    # extrudeFeature2 = extrudes.add(extInput2)

                    # export the component one by one with a specified format
                    for comp in allComps:
                        compName = comp.name
                        fileName = scriptDir + "/test2D_" + \
                            str(num) + '_pts_' + str(putty_depth) + "_depth_" + str(numGeom)

                        # export the component with STP format
                        # stpOptions = exportMgr.createSTEPExportOptions(fileName, comp)
                        # exportMgr.execute(stpOptions)
                    sketch.saveAsDXF(fileName + '.dxf')
                    area_top = graphite_width*graphite_thickness/2 - area
                    area_bottom = graphite_width*graphite_thickness/2 - area2  # areas are currently in cm^2

                    with open(textfile, 'a') as f:
                        f.write(str(fileName) + '.dxf' + ',' + str(num) + ',' + str(putty_depth) + ',' +
                                str(area_top) + ',' + str(area_bottom) + ',' + str(putty_area) + '\n')

                    # extrudeFeature.deleteMe()
                    # extrudeFeature2.deleteMe()
                    sketch.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
