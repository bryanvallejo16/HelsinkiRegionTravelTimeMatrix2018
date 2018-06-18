# -*- coding: utf-8 -*-
"""
Plot best 10 % accessibility areas.

Requirements:
    geopandas-1.0.0.dev
    shapely-1.6.2
    matplotlib-2.0.0
    

Created on:
    June 16th 2018

Author:
    Henrikki Tenkanen, Digital Geography Lab, University of Helsinki
    
"""
import geopandas as gpd
import os
import matplotlib.pyplot as plt
from shapely.ops import polygonize
from shapely.geometry import MultiPolygon
import matplotlib.patches as patches

def create_custom_legend(ax, xleft_lim, yup_lim):

    # Create custom legend for the plot
    bwidht = 3000
    bheight = 1300
    
    # Legend box for Car, PT and Bike
    ptxy = (xleft_lim + 4000 + 500, yup_lim - 1500)
    carxy = (xleft_lim + 4000 + 500*10, yup_lim - 1500)
        
    ptbox = patches.Rectangle(xy=ptxy, width=bwidht, height=bheight, facecolor=pt_color, alpha=alpha)
    carbox = patches.Rectangle(xy=carxy, width=bwidht, height=bheight, facecolor=car_color, alpha=alpha)
        
#    ax.text(x=ptxy[0]+ 450, y=ptxy[1] + 2000, s="PT", family=ffamily, weight=fweight, fontsize=fsize)
#    ax.text(x=carxy[0]+ 450, y=carxy[1] + 2000, s="Car", family=ffamily, weight=fweight, fontsize=fsize)
#    ax.text(x=bikexy[0]+ 400, y=bikexy[1] + 2000, s="Bike", family=ffamily, weight=fweight, fontsize=fsize)
    
    # Legend boxes for combinations of Car, PT, and Bike
    # Car + PT
    xycp = (xleft_lim + 500*10*5, yup_lim - 1500)
    carpt_box_c = patches.Rectangle(xy=xycp, width=bwidht, height=bheight, facecolor=car_color, alpha=alpha)
    carpt_box_p = patches.Rectangle(xy=xycp, width=bwidht, height=bheight, facecolor=pt_color, alpha=alpha)
    
    
    
    # Add the patches to the Axes
    ax.add_patch(ptbox)
    ax.add_patch(carbox)
    
    ax.add_patch(carpt_box_c)
    ax.add_patch(carpt_box_p)
    
    return ax
    
def plot_most_accessible_overlaps(outfp):
    # Plot everything on top of each other
    ax = car.plot(color=car_color, alpha=alpha)
    ax = pt.plot(ax=ax, color=pt_color, alpha=alpha)
    ax = plot_environment(ax=ax)
    
    # X and y limits for the map
    xleft_lim, xright_lim = 360900, 404000
    ylow_lim, yup_lim = 6665000, 6699900
    
    # Create custom legend for the map
    ax = create_custom_legend(ax, xleft_lim=xleft_lim, yup_lim=yup_lim)
    
    # Set x/y limits
    ax.set_xlim([xleft_lim, xright_lim])
    ax.set_ylim([ylow_lim, yup_lim])
    plt.axis('off')
    #plt.tight_layout()
    plt.savefig(outfp, dpi=500)
    
def plot_environment(ax):
    ax = borders.plot(ax=ax, facecolor='none', lw=0.7, edgecolor='gray', linestyle='--')
    ax = coast.plot(ax=ax, color=water_color, linewidth=0)
    ax = roads.plot(ax=ax, lw=1.0, color=roads_color, alpha=0.8)
    ax = metro.plot(ax=ax, lw=1.5, color=metro_color)
    ax = rails.plot(ax=ax, lw=1.25, linestyle='-', color='white')
    ax = rails.plot(ax=ax, lw=1.25, linestyle='--', color=rail_color)
    ax = lakes.plot(ax=ax, color=water_color, linewidth=0)
    return ax
    
    
def plot_most_accessible_10_percent(df, column, edgecolor, lw, linestyle='-', scheme=None, alpha=1.0, cmap="RdYlBu", legend=False, legend_anchor=None, outfp=None, title=None):
    # Plot travel mode
    if legend:
        ax = df.plot(column=column, edgecolor=edgecolor, lw=lw, linestyle=linestyle, cmap=cmap, alpha=alpha, scheme=scheme, legend=True, legend_kwds={'title': title,'ncol': 3, 'bbox_to_anchor': (1.03, 0.07), 'framealpha': 1.0})
    else:
        ax = df.plot(column=column, edgecolor=edgecolor, lw=lw, linestyle=linestyle, cmap=cmap, alpha=alpha, scheme=scheme)
    # Plot surroundings
    ax = plot_environment(ax=ax)
    
    # Location of legend
    if legend_anchor:
        # TODO
        pass
    
    # X and y limits for the map
    xleft_lim, xright_lim = 360900, 404000
    ylow_lim, yup_lim = 6665000, 6699900
    
    
    # Set x/y limits
    ax.set_xlim([xleft_lim, xright_lim])
    ax.set_ylim([ylow_lim, yup_lim])
    plt.axis('off')
    plt.savefig(outfp, dpi=500)
    return ax

# Filepaths
data_dir = r"C:\HY-DATA\HENTENKA\KOODIT\Matrix2018\data"
carr_fp = os.path.join(data_dir, "Car_r_best_10_percent_2015.shp")
ptr_fp = os.path.join(data_dir, "PT_r_best_10_percent_2015.shp")
roads_fp = os.path.join(data_dir, "main_roads.shp")
metro_fp = os.path.join(data_dir, "Full_metro_line_eastWest.shp")
coast_fp = os.path.join(data_dir, "rantaviiva_polygon.shp")
rails_fp = os.path.join(data_dir, "Full_railway.shp")
lakes_fp = os.path.join(data_dir, "lakes.shp")
borders_fp = os.path.join(data_dir, "city_borders.shp")

# Output filepaths
overlap_out = r"C:\HY-DATA\HENTENKA\KOODIT\Matrix2018\Figures\Overlap\2015_All_modes_rushHour_best_10_percent_areas.png"
pt_out = r"C:\HY-DATA\HENTENKA\KOODIT\Matrix2018\Figures\Individual\2015_PT_most_accessible_10_percent.png"
car_out = r"C:\HY-DATA\HENTENKA\KOODIT\Matrix2018\Figures\Individual\2015_Car_most_accessible_10_percent.png"

# Read files
car = gpd.read_file(carr_fp)
pt = gpd.read_file(ptr_fp)
roads = gpd.read_file(roads_fp)
metro = gpd.read_file(metro_fp)
coast = gpd.read_file(coast_fp)
rails = gpd.read_file(rails_fp)
lakes = gpd.read_file(lakes_fp)
borders = gpd.read_file(borders_fp)

# Ensure the same projection
CRS = car.crs
pt = pt.to_crs(CRS)
metro = metro.to_crs(CRS)
roads = roads.to_crs(CRS)
coast = coast.to_crs(CRS)
rails = rails.to_crs(CRS)
lakes = lakes.to_crs(CRS)
borders = borders.to_crs(CRS)

# Merge coastline polygons
coast = gpd.GeoDataFrame([[coast.unary_union]], columns=['geometry'], crs=CRS)

# Parameters
car_colormap = None
car_color = 'blue'
pt_color = 'red'
metro_color = 'red'
rail_color = 'black'
alpha = 0.7
#scheme = "quantiles"
water_color = '#808080'
roads_color = "#404040"
bike_ecolor = 'orange'
bike_fcolor = 'none'

# Font family
ffamily = 'Arial'
fsize = 7
fweight = 'normal'

# Overlap
plot_most_accessible_overlaps(outfp = overlap_out)

# Individual modes
plot_most_accessible_10_percent(df=pt, column='ptrmedian', scheme='fisher_jenks', edgecolor='gray', lw=0.1, outfp=pt_out, legend=True, title='Mediaani matka-aika (min) joukkoliikenteellä')
plot_most_accessible_10_percent(df=car, column='carrmedian', scheme='fisher_jenks', edgecolor='gray', lw=0.1, outfp=car_out, legend=True, title='Mediaani matka-aika (min) autolla')
