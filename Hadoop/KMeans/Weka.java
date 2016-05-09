import java.awt.BorderLayout;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import javax.swing.JFrame;

import weka.clusterers.ClusterEvaluation;
import weka.clusterers.SimpleKMeans;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ArffSaver;
import weka.core.converters.CSVLoader;
import weka.gui.explorer.ClustererAssignmentsPlotInstances;
import weka.gui.visualize.PlotData2D;
import weka.gui.visualize.VisualizePanel;

public class Weka {
	
	public static void main(String[] args) throws Exception {
		
		int numOfClusters = Integer.parseInt(args[0]);
		String attribute1 = args[1];
		String attribute2 = args[2];
		/**
		 * Read File
		 */
		BufferedReader bufferedReader = new BufferedReader(new FileReader("Dataset.arff"));
		Instances data = new Instances(bufferedReader);
		
		/**
		 * Remove unnecessary columns here
		 */
		String[] allAttributes = new String[]{"DRG","id","NAME","STREET","CITY","ZIP","REFERRAL","COREVED CHARGES","TOTAL CHARGES","MEDICARE", "STATE", "DISCHARGES"};
		for(String attr: allAttributes){
			if(!attr.equals(attribute1) && !attr.equals(attribute2))
				data.deleteAttributeAt(data.attribute(attr).index());
		}
		
		SimpleKMeans kMeans = new SimpleKMeans();
		kMeans.setNumClusters(numOfClusters);
		kMeans.setSeed(10);
		kMeans.setPreserveInstancesOrder(true);
		kMeans.buildClusterer(data);
		
		ClusterEvaluation clusterEvaluation = new ClusterEvaluation();
		clusterEvaluation.setClusterer(kMeans);
		clusterEvaluation.evaluateClusterer(data);
		System.out.println(clusterEvaluation.clusterResultsToString());
		
		ClustererAssignmentsPlotInstances plotInstances = new ClustererAssignmentsPlotInstances();
		plotInstances.setClusterer(kMeans);
		plotInstances.setInstances(data);
		plotInstances.setClusterEvaluation(clusterEvaluation);
		plotInstances.setUp();
		
		String name = (new SimpleDateFormat("HH:mm:ss - ")).format(new Date());
	    String cname = kMeans.getClass().getName();
	    if (cname.startsWith("weka.clusterers."))
	      name += cname.substring("weka.clusterers.".length());
	    else
	      name += cname;
	    
	    name = name + " (" + data.relationName() + ")";
	    
	    VisualizePanel vp = new VisualizePanel();
	    vp.setName(name);
	    vp.addPlot(plotInstances.getPlotData(cname));

	    // display data
	    // taken from: ClustererPanel.visualizeClusterAssignments(VisualizePanel)
	    JFrame jf = new JFrame("Weka Clusterer Visualize: " + vp.getName());
	    jf.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
	    jf.setSize(500, 400);
	    jf.getContentPane().setLayout(new BorderLayout());
	    jf.getContentPane().add(vp, BorderLayout.CENTER);
	    jf.setVisible(true);	
	}
}