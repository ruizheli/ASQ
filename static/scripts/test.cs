//css_reference System.Windows.Forms;
using System;
using System.Windows.Forms;
 
class Script
{
     static public void Main(string[] args)
     {
        for (int i = 0; i < args.Length; i++)
            Console.WriteLine(args[i]);
     
         MessageBox.Show("Just a test!");
     }
}
