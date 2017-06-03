from flask import Flask, render_template

app=Flask(__name__)

@app.route('/plot/')
def plot():
    from getData import getData
    from bokeh.plotting import figure, output_file, show
    from bokeh.embed import components
    from bokeh.resources import CDN
    
    def inc_dec(c, o):
        if c > o:
            value = 'Increase'
        elif c < o:
            value = 'Decrease'
        else:
            value = 'Equal'
        return value
    
    df = getData()
    df['Status'] = [inc_dec(c,o) for c, o in zip(df.Close, df.Open)]
    df['Middle'] = (df.Open + df.Close)/2
    df['Height'] = abs(df.Open - df.Close)
    
    p = figure(x_axis_type='datetime', width=1000, height=300)
    p.title = 'Candlestick chart'
    
    hours_12 = 12*60*60*1000
    
    p.segment(df.index, df.High, df.index, df.Low, color='black')
    p.rect(df.index[df.Status=='Increase'], df.Middle[df.Status=='Increase'], hours_12,
           df.Height[df.Status=='Increase'], fill_color='green', line_color='black')  
    p.rect(df.index[df.Status=='Decrease'], df.Middle[df.Status=='Decrease'], hours_12,
           df.Height[df.Status=='Decrease'], fill_color='red', line_color='black')
    
    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("plot.html", script1=script1, div1=div1,
                           cdn_css=cdn_css, cdn_js=cdn_js)



@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
