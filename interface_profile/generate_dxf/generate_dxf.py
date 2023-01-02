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
        # num_spline_points = 10
        total_num_geom = 10

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

        textfile = scriptDir + "/" + 'data' + '.csv'

        with open(textfile, 'w') as f:
            f.write('filename,num_point,pore_depth,area_top,area_bottom,max_depth_top,max_depth_bottom\n')

        with open('/Users/shomikverma/Documents/GitHub/graphite-modeling/fusion add-in/graphite_points.csv', 'r') as file:
            data = file.readlines()

        for i in range(len(data)):
            if i == 0:
                continue
            points = [x.replace('"', '').replace(']', '').replace('[', '') for x in data[i].strip().split(',')]
            num_spline_points = int(points[-2])
            putty_depth = float(points[-1])
            xs = [float(x) for x in points[:num_spline_points+1]]
            ys_bottom = [float(x) for x in points[(num_spline_points+1):2*(num_spline_points+1)]]
            ys_top = [float(x) for x in points[2*(num_spline_points+1):3*(num_spline_points+1)]]

            des = app.activeProduct
            # Get the root component of the active design.
            rootComp = des.rootComponent
            # Create a new sketch on the xy plane.
            sketches = rootComp.sketches
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)

            # create left line boundary of graphite
            left_side = adsk.core.ObjectCollection.create()
            left_side.add(adsk.core.Point3D.create(xs[0], ys_bottom[0], 0))
            left_side.add(adsk.core.Point3D.create(xs[0], ys_top[0], 0))
            sketch.sketchCurves.sketchFittedSplines.add(left_side)

            # create right line boundary of graphite
            right_side = adsk.core.ObjectCollection.create()
            right_side.add(adsk.core.Point3D.create(xs[-1], ys_bottom[-1], 0))
            right_side.add(adsk.core.Point3D.create(xs[-1], ys_top[-1], 0))
            sketch.sketchCurves.sketchFittedSplines.add(right_side)

            # create middle line
            mid_line = adsk.core.ObjectCollection.create()
            mid_line.add(adsk.core.Point3D.create(0, ys_top[0]/2, 0))
            mid_line.add(adsk.core.Point3D.create(xs[-1], ys_top[-1]/2, 0))
            sketch.sketchCurves.sketchFittedSplines.add(mid_line)

            points_bottom = adsk.core.ObjectCollection.create()  # Create an object collection for the points.
            points_top = adsk.core.ObjectCollection.create()

            # Enter variables here. E.g. E = 50
            # startRange = 0  # Start of range to be evaluated.
            # endRange = graphite_width  # End of range to be evaluated.
            # splinePoints = num  # Number of points that splines are generated.
            # WARMING: Using more than a few hundred points may cause your system to hang.

            # make the spline start at origin
            points_bottom.add(adsk.core.Point3D.create(xs[0], ys_bottom[0], 0))

            points_top.add(adsk.core.Point3D.create(xs[0], ys_top[0], 0))

            # area = areaProps.area

            for j in range(1, len(xs)-1):
                # t = startRange + ((endRange - startRange)/splinePoints)*i
                # xCoord = t
                # yCoord_bottom = random.uniform(0, putty_depth)
                # yCoord_top = random.uniform(graphite_thickness - putty_depth, graphite_thickness)
                zCoord = 0
                points_bottom.add(adsk.core.Point3D.create(xs[j], ys_bottom[j], zCoord))
                points_top.add(adsk.core.Point3D.create(xs[j], ys_top[j], zCoord))

            # make the splines come back to end point
            points_bottom.add(adsk.core.Point3D.create(xs[-1], ys_bottom[-1], 0))
            points_top.add(adsk.core.Point3D.create(xs[-1], ys_top[-1], 0))

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
                fileName = scriptDir + "/dxf_geometries/test2D_" + \
                    str(num_spline_points) + '_pts_' + str(putty_depth) + "_depth_" + str(i % total_num_geom)

                # export the component with STP format
                # stpOptions = exportMgr.createSTEPExportOptions(fileName, comp)
                # exportMgr.execute(stpOptions)
            sketch.saveAsDXF(fileName + '.dxf')
            # area_top = graphite_width*graphite_thickness/2 - area
            # area_bottom = graphite_width*graphite_thickness/2 - area2  # areas are currently in cm^2

            with open(textfile, 'a') as f:
                f.write(str(fileName) + '.dxf' + ',' + str(num_spline_points) + ',' +
                        str(putty_depth) + ',' + str(area) + ',' + str(area2) + ',' + str(max(ys_bottom)) + ',' + str(min(ys_top)) + '\n')

            # extrudeFeature.deleteMe()
            # extrudeFeature2.deleteMe()
            sketch.deleteMe()

        textfile = scriptDir + "/" + 'data_S3' + '.csv'

        with open(textfile, 'w') as f:
            f.write('filename,num_point,pore_depth,area_top,area_bottom,max_depth_top,max_depth_bottom\n')

        with open('/Users/shomikverma/Documents/GitHub/graphite-modeling/fusion add-in/graphite_points_S3.csv', 'r') as file:
            data = file.readlines()
        
        if not os.path.isdir(scriptDir + "/S3_geometries"):
            os.mkdir(scriptDir + "/S3_geometries")

        for i in range(len(data)):
            if i == 0:
                continue
            points = [x.replace('"', '').replace(']', '').replace('[', '') for x in data[i].strip().split(',')]
            num_spline_points = int(points[-2])
            putty_depth = float(points[-1])
            xs = [float(x) for x in points[:num_spline_points+1]]
            ys_bottom = [float(x) for x in points[(num_spline_points+1):2*(num_spline_points+1)]]
            ys_top = [float(x) for x in points[2*(num_spline_points+1):3*(num_spline_points+1)]]

            des = app.activeProduct
            # Get the root component of the active design.
            rootComp = des.rootComponent
            # Create a new sketch on the xy plane.
            sketches = rootComp.sketches
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)

            # create left line boundary of graphite
            left_side = adsk.core.ObjectCollection.create()
            left_side.add(adsk.core.Point3D.create(xs[0], ys_bottom[0], 0))
            left_side.add(adsk.core.Point3D.create(xs[0], ys_top[0], 0))
            sketch.sketchCurves.sketchFittedSplines.add(left_side)

            # create right line boundary of graphite
            right_side = adsk.core.ObjectCollection.create()
            right_side.add(adsk.core.Point3D.create(xs[-1], ys_bottom[-1], 0))
            right_side.add(adsk.core.Point3D.create(xs[-1], ys_top[-1], 0))
            sketch.sketchCurves.sketchFittedSplines.add(right_side)

            # create middle line
            mid_line = adsk.core.ObjectCollection.create()
            mid_line.add(adsk.core.Point3D.create(0, ys_top[0]/2, 0))
            mid_line.add(adsk.core.Point3D.create(xs[-1], ys_top[-1]/2, 0))
            sketch.sketchCurves.sketchFittedSplines.add(mid_line)

            points_bottom = adsk.core.ObjectCollection.create()  # Create an object collection for the points.
            points_top = adsk.core.ObjectCollection.create()

            # Enter variables here. E.g. E = 50
            # startRange = 0  # Start of range to be evaluated.
            # endRange = graphite_width  # End of range to be evaluated.
            # splinePoints = num  # Number of points that splines are generated.
            # WARMING: Using more than a few hundred points may cause your system to hang.

            # make the spline start at origin
            points_bottom.add(adsk.core.Point3D.create(xs[0], ys_bottom[0], 0))

            points_top.add(adsk.core.Point3D.create(xs[0], ys_top[0], 0))

            # area = areaProps.area

            for j in range(1, len(xs)-1):
                # t = startRange + ((endRange - startRange)/splinePoints)*i
                # xCoord = t
                # yCoord_bottom = random.uniform(0, putty_depth)
                # yCoord_top = random.uniform(graphite_thickness - putty_depth, graphite_thickness)
                zCoord = 0
                points_bottom.add(adsk.core.Point3D.create(xs[j], ys_bottom[j], zCoord))
                points_top.add(adsk.core.Point3D.create(xs[j], ys_top[j], zCoord))

            # make the splines come back to end point
            points_bottom.add(adsk.core.Point3D.create(xs[-1], ys_bottom[-1], 0))
            points_top.add(adsk.core.Point3D.create(xs[-1], ys_top[-1], 0))

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
                fileName = scriptDir + "/S3_geometries/test2D_" + \
                    str(num_spline_points) + '_pts_' + str(putty_depth) + "_depth_" + str(i % total_num_geom)

                # export the component with STP format
                # stpOptions = exportMgr.createSTEPExportOptions(fileName, comp)
                # exportMgr.execute(stpOptions)
            sketch.saveAsDXF(fileName + '.dxf')
            # area_top = graphite_width*graphite_thickness/2 - area
            # area_bottom = graphite_width*graphite_thickness/2 - area2  # areas are currently in cm^2

            with open(textfile, 'a') as f:
                f.write(str(fileName) + '.dxf' + ',' + str(num_spline_points) + ',' +
                        str(putty_depth) + ',' + str(area) + ',' + str(area2) + ',' + str(max(ys_bottom)) + ',' + str(min(ys_top)) + '\n')

            # extrudeFeature.deleteMe()
            # extrudeFeature2.deleteMe()
            sketch.deleteMe()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
