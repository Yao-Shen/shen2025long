import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from scipy.interpolate import interp1d

def interp(xf, x, y):
    """ 1D interp """
    f = interp1d(x, y, bounds_error=False, fill_value=np.nan)
    return f(xf)

def make_theme(ax, logx=False, logy=False, grid=False, minorx=2, minory=2, ticklength=6, lw=0.5):
    """ Apply the theme for figures
    
    Parameters
    ----------
    ax :  AxesSubplot
        AxesSubplot axes.
    logx :  bool
        Where use log scale for x axis (default: False).
    logy :  bool
        Where use log scale for y axis (default: False).
    grid :  bool, string, list or dict
        Grid parameters. If False, grid will not show (True not supported).
        If string, it will be used as line style for grid of major ticks.
        If list, it will be used as line styles for grid of major and minor ticks, respectively.
        If dict, it can contain some of the keys including 'lw', 'ls' and 'color',
            each of which can be either a string or a list.
            If one of them is given as a list, minor grid lines will be shown (default: False).
    minorx :  bool, int
        Whether to show minor x ticks. If False, it will not show (True not supported, default: 2)
    minory :  bool, int
        Whether to show minor y ticks. If False, it will not show (True not supported, default: 2)
    ticklength :  int
        Length of axis ticks (default: 6).
    lw :  float
        Line width for both the ticks and frame (default: 0.5).
    """
    if logx:
        ax.set_xscale('log')
        minorx = False
    if minorx:
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(int(minorx)))
    if logy:
        ax.set_yscale('log')
        minory = False
    if minory:
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(int(minory)))
    if not logx and not logy:
        ax.ticklabel_format(useOffset=False, style='plain')
    if grid:
        ngrid = 1
        if isinstance(grid, dict):
            if 'ls' not in grid.keys():
                gls = ['--', '--']
            elif isinstance(grid['ls'], list):
                gls = grid['ls']
                ngrid = 2
            else:
                gls = [grid['ls'], grid['ls']]
            if 'lw' not in grid.keys():
                glw = [0.5, 0.5]
            elif isinstance(grid['lw'], list):
                glw = grid['lw']
                ngrid = 2
            else:
                glw = [grid['lw'], grid['lw']]
            if 'color' not in grid.keys():
                gcolor = ['gray', 'lightgray']
            elif isinstance(grid['color'], list):
                gcolor = grid['color']
                ngrid = 2
            else:
                gcolor = [grid['color'], grid['color']]
        elif isinstance(grid, list):
            gls = grid
            ngrid = 2
            glw = [0.5, 0.5]
            gcolor = ['gray', 'lightgray']
        else:
            gls = [grid, grid]
            glw = [0.5, 0.5]
            gcolor = ['gray', 'lightgray']
        ax.grid(ls=gls[0], color=gcolor[0], lw=glw[0], which='major')
        if ngrid==2:
            ax.grid(ls=gls[1], color=gcolor[1], lw=glw[1], which='minor')
    
    ax.tick_params(which='major', direction='in', left=True, bottom=True, top=True, right=True, width=lw, length=ticklength)
    ax.tick_params(which='minor', direction='in', left=minory, bottom=minorx, top=minorx, right=minory, width=lw, length=ticklength/2)
#    ax.ticklabel_format(useOffset=False, style='plain')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(lw)

def plot_image(image, x=None, y=None, ax=None, cax=None, imshow=False,
               vmin=None, vmax=None, pmin=1, pmax=99, aspect='auto',
               cbar=False, cbar_label=None, cmap='viridis'):
    """ Plot 2D Image.
    
    Parameters
    ----------
    image :  2d array, image to plot.
    x :  1d array, list of x axis coordinates. If None, imshow is called (default: None).
    y :  1d array, list of y axis coordinates. If None, imshow is called (default: None).
    ax :  AxesSubplot, ax to plot main figure. If None, a new ax will be made (default: None).
    cax :  AxesSubplot, ax to plot colorbar. If None, colorbar will be plot in ax (default: None).
    imshow :  bool, enforce imshow function even if x or y is given (default: False).
    vmin, vmax :  float, data range that the colormap covers. If None, they will be determined by pmin and pmax (default: None).
    pmin, pmax :  float, data percentage rage that the colormap covers (default: 1).
    aspect :  str or array, the aspect ratio of the Axes (default: auto).
    cbar :  bool, plot the colorbar (default: False).
    cbar_label :  str, label of colorbar (default: None).
    cmap :  str, colormap (default: viridis).
    
    Returns
    -------
    ax, art, cart if cbar is True
    ax, art if cbar is False
    """
    if ax is None:
        fig, ax = plt.subplots()
    if vmin == None:
        vmin = np.nanpercentile(image, pmin)
    if vmax == None:
        vmax = np.nanpercentile(image, pmax)
    if x is None or y is None:
        imshow = True
    if imshow:
        if x is None and y is None:
            art = ax.imshow(image, vmin=vmin, vmax=vmax, interpolation=None, aspect=aspect, origin=None, cmap=cmap, rasterized=True)
        elif x is None:
            art = ax.imshow(image, vmin=vmin, vmax=vmax, interpolation=None, aspect=aspect, origin='lower', cmap=cmap, rasterized=True,
                            extent=[0, np.array(image).shape[1]-1, np.min(y), np.max(y)])
        elif y is None:
            art = ax.imshow(image, vmin=vmin, vmax=vmax, interpolation=None, aspect=aspect, origin='lower', cmap=cmap, rasterized=True,
                            extent=[np.min(x), np.max(x), 0, np.array(image).shape[0]-1])
        else:
            art = ax.imshow(image, vmin=vmin, vmax=vmax, interpolation=None, aspect=aspect, origin='lower', cmap=cmap, rasterized=True,
                            extent=[np.min(x), np.max(x), np.min(y), np.max(y)])
    else:
        if x is None:
            x = np.arange(np.array(image).shape[1])
        if y is None:
            y = np.arange(np.array(image).shape[0])
        art = ax.pcolormesh(enlarge(x), enlarge(y), image, vmin=vmin, vmax=vmax, cmap=cmap, rasterized=True)
        ax.axis(aspect)
    if cbar:
        if cax is None:
            cart = plt.colorbar(art, ax=ax)
        else:
            cart = plt.colorbar(art, cax=cax)
        if cbar_label is not None:
            cart.set_label(cbar_label)
        cart.outline.set_linewidth(0.5)
        return ax, art, cart
    else:
        return ax, art

def enlarge(x0):
    """ Extend the axis: enlarge(vector) """
    if isinstance(x0, list):
        x = np.array(x0)
    else:
        x = x0-0
    new_x = np.zeros(np.size(x)+1)
    new_x[1:-1] = (x[1:]+x[:-1])/2
    new_x[0] = 3./2.*x[0]-1./2.*x[1]
    new_x[-1] = 3./2.*x[-1]-1./2.*x[-2]
    return new_x

def genlattice(params):
    """
    Generate the lattice vectors.

    Parameters
    ----------
    params :  lattice parameters [a,b,c,alpha,beta,gamma] in unit of \AA and degree.
    
    Returns
    ----------
    latticeV :  {'a','b','c','as','bs','cs','av','bv','cv','asv','bsv','csv','avn','bvn','cvn','asvn','bsvn','csvn','V','Vs'}
                's' denotes star, 'v' denotes vector, 'V' denotes volume, 'n' denotes normalized.
                'a' direction is used as x axis, and 'b' in xy plane.
    
    Example
    -------
    >>> crystal = genlattice([3.5,3.5,25.5,90.,90.,90.])
    """
    a = params[0]
    b = params[1]
    c = params[2]
    alpha = params[3]/180*np.pi
    beta  = params[4]/180*np.pi
    gamma = params[5]/180*np.pi
    
    avn = [1,0,0]
    bvn = [np.cos(gamma), np.sin(gamma), 0]
    cvn = [np.cos(beta),  (np.cos(alpha)-np.cos(beta)*np.cos(gamma))/np.sin(gamma), 0]
    cvn[2] = np.sqrt(np.sin(beta)**2-cvn[1]**2)
    
    av = np.dot(a,avn)
    bv = np.dot(b,bvn)
    cv = np.dot(c,cvn)
    
    V = np.dot(np.cross(av, bv), cv)
    
    asv = 2*np.pi*np.cross(bv,cv)/V
    bsv = 2*np.pi*np.cross(cv,av)/V
    csv = 2*np.pi*np.cross(av,bv)/V
    
    asvn = np.dot(asv, 1/np.linalg.norm(asv))
    bsvn = np.dot(bsv, 1/np.linalg.norm(bsv))
    csvn = np.dot(csv, 1/np.linalg.norm(csv))
    
    Vs = np.dot(np.cross(asv, bsv), csv)
    
    latticeV = {'a':a, 'b':b, 'c':c, 'as':np.linalg.norm(asv), 'bs':np.linalg.norm(bsv), 'cs':np.linalg.norm(csv), 'av':av, 'bv':bv, 'cv':cv, 'asv':asv, 'bsv':bsv, 'csv':csv, 'avn':avn, 'bvn':bvn, 'cvn':cvn, 'asvn':asvn, 'bsvn':bsvn, 'csvn':csvn, 'V':V, 'Vs':Vs}
    
    return latticeV


def unicorn(value, unit, par='xray'):
    """
    Convert the unit.

    Parameters
    ----------
    value & unit:  value (float) and corresponding unit (string) or quantity (string)
    par :  particle name, xray or neutron
    
    Returns
    ----------
    dictionary :  {'wavelength', 'energy', 'wavevector', 'frequency', 'wavenumber', 'velocity', 'temperature', 'time'}
          unit :         A          meV         A-1           THz          cm-1         km/s           K         ps
    
    Example
    -------
    >>> unicorn(870e3, 'meV')
    """
    params = {}
    if par=='neutron':
        if (unit=='wavelength') | (unit=='A'):
            params['energy'] = (9.044/value)**2
        elif (unit=='energy') | (unit=='meV'):
            params['energy'] = value
        elif (unit=='wavevector') | (unit=='A-1'):
            params['energy'] = 2.072*value**2
        elif (unit=='frequency') | (unit=='THz'):
            params['energy'] = value/0.2418
        elif (unit=='wavenumber') | (unit=='cm-1'):
            params['energy'] = value*2.998/24.18
        elif (unit=='velocity') | (unit=='km/s'):
            params['energy'] = value**2*5.2171
        elif (unit=='temperature') | (unit=='K'):
            params['energy'] = value/11.605
        elif (unit=='time') | (unit=='ps'):
            params['energy'] = 1/value/0.2418
        
        params['wavelength'] = 9.044/np.sqrt(params['energy'])
        params['wavevector'] = np.sqrt(params['energy']/2.072)
        params['frequency'] = 0.2418*params['energy']
        params['wavenumber'] = params['energy']/2.998*24.18
        params['velocity'] = np.sqrt(params['energy']/5.2171)
        params['temperature'] = params['energy']*11.605
        params['time'] = 1/0.2418/params['energy']
        
    else:
        if (unit=='wavelength') | (unit=='A'):
            params['energy'] = 12.398e6/value
        elif (unit=='energy') | (unit=='meV'):
            params['energy'] = value
        elif (unit=='wavevector') | (unit=='A-1'):
            params['energy'] = 12.398e6/2/np.pi*value
        elif (unit=='frequency') | (unit=='THz'):
            params['energy'] = value/2.998*12.398
        elif (unit=='wavenumber') | (unit=='cm-1'):
            params['energy'] = 12.398e-2*value
        elif (unit=='temperature') | (unit=='K'):
            params['energy'] = value/11.605
        elif (unit=='time') | (unit=='ps'):
            params['energy'] = 12.398/2.998/value
            
        params['wavelength'] = 12.398e6/params['energy']
        params['wavevector'] = 2*np.pi/12.398e6*params['energy']
        params['frequency'] = params['energy']*2.998/12.398
        params['wavenumber'] = params['energy']/12.398e-2
        params['temperature'] = params['energy']*11.605
        params['time'] = 12.398/2.998/params['energy']
        
    return params