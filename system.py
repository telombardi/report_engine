import report_functions as rf
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import seaborn as sns
import matplotlib.pyplot as plt

class Report:
    
    def __init__(self, output):
        '''Organizes data and configuration required for the report.'''
        self.output = output
        self.python_version = rf.get_python_version()
        self.cpu_block = rf.get_cpu_block()
        self.hostname = rf.gethostname()
        self.date = rf.getdate()
        self.os_type = rf.getsystemtype()
        self.os_version = rf.getuname()
        self.environment = Environment(loader=FileSystemLoader("templates/"))
        self.template = self.environment.get_template("system_report_template.html")
        self.disk_used = rf.get_disk_usage_used()
        self.disk_free = rf.get_disk_usage_free()
        self.disk_percent = rf.get_disk_usage_percent()
        self.disk_used_bytes = rf.get_disk_usage_used_bytes()
        self.disk_free_bytes = rf.get_disk_usage_free_bytes()
        self.memory_used = rf.get_used_mem()
        self.memory_free = rf.get_available_mem()
        self.memory_percent = rf.get_percent_mem()
        self.memory_used_bytes = rf.get_used_mem_bytes()
        self.memory_free_bytes = rf.get_available_mem_bytes()
        self.mount_points = rf.get_mount_points()
        self.mac = rf.getmac()
        self.nets = rf.getinterfaces()
        self.python_packages = rf.get_python_packages()
        self.folder = self.hostname+"_report_"+self.date
        self.filename = self.folder+".html"
        self.fullfolder = Path(self.output,self.folder)
        self.fulloutput = Path(self.output,self.filename)
        
    def run(self):
        '''Runs and outputs the report.'''
        #load additional modules here if necessary
        #create folder for output
        try:
          os.mkdir(self.fullfolder)
        except FileExistsError:
          pass
        
        #create image for memory
        data = [self.memory_used_bytes,self.memory_free_bytes]
        labels = ['Used: '+self.memory_used,'Free: '+self.memory_free]
        colors = ['#FF0000', '#0000FF']
        sns.set_style('whitegrid')
        plt.figure(figsize=(3,3))
        
        plt.pie(data, labels=labels, colors=colors)
        # draw circle
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
 
        # Adding Circle in Pie chart
        fig.gca().add_artist(centre_circle)
 
        # Adding Title of chart
        plt.title('Memory Usage: '+str(self.memory_percent)+'%',fontsize=24)
        plt.savefig(Path(self.fullfolder,'memory_usage.png'),bbox_inches='tight')
        
        #create image for disk
        data = [self.disk_used_bytes,self.disk_free_bytes]
        labels = ['Used: '+self.disk_used, 'Free: '+self.disk_free]
        colors = ['#FF0000', '#0000FF']
        sns.set_style('whitegrid')
        plt.figure(figsize=(3,3))
        plt.pie(data, labels=labels, colors=colors)
        # draw circle
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
 
        # Adding Circle in Pie chart
        fig.gca().add_artist(centre_circle)
 
        # Adding Title of chart
        plt.title('Disk Usage: '+str(self.disk_percent)+'%',fontsize=24)
        plt.savefig(Path(self.fullfolder,'disk_usage.png'),bbox_inches='tight')
        
        # Construct mount point table
        mps = ''
        for mount in self.mount_points:
          fields = mount.split(',')
          mps = mps+'<tr>'
          for f in fields:
            mps = mps + '<td>' + f + '</td>'
          mps = mps + '</tr>\n'
        
        # Construct net interface table
        net_table = ''
        for i in self.nets:
          fields = i.split(',')
          net_table = net_table+'<tr>'
          for f in fields:
            net_table = net_table+'<td>'+f+'</td>'
          net_table = net_table+'</tr>\n'
        
        # Construct python packages
        python_table = ''
        for m in self.python_packages:
          python_table=python_table+'<tr><td>'+m+'</td></tr>\n'
          
        # Output data to report template  
        content = self.template.render(
            date=self.date,
            server=self.hostname,
            os_type=self.os_type,
            os_version=self.os_version,
            python_version=self.python_version,
            disk_used=self.disk_used,
            disk_free=self.disk_free,
            disk_png=Path(self.folder,'disk_usage.png'),
            memory_used=self.memory_used,
            memory_free=self.memory_free,
            memory_png=Path(self.folder,'memory_usage.png'),
            cpu=self.cpu_block,
            mount_points=mps,
            mac=self.mac,
            nets=net_table,
            python_packages=python_table
        )
        
        # Output report
        with open(self.fulloutput, mode='w', encoding='utf-8') as report:
            report.write(content)
        
        
    def save_json(self):
        pass
    
    
        