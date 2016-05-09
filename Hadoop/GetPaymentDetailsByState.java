import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class GetPaymentDetailsByState {
	
	public static class PaymentsMapper extends Mapper<LongWritable, Text, Text, PaymentsWritable> {
		
		@Override
		protected void map(LongWritable key, Text value, Context context)
				throws IOException, InterruptedException {
			// TODO Auto-generated method stub
			String array[] = value.toString().trim().replaceAll("\\$","").split(",(?=([^\"]*\"[^\"]*\")*[^\"]*$)");
			System.out.println(value.toString().trim().replaceAll("\\$",""));
			//Data Format State = 5, Covered Charges = 9, Total = 10
			String state = array[5];
			float coveredCharges = Float.parseFloat(array[9]);
			float totalCharges = Float.parseFloat(array[10]);
			PaymentsWritable p = new PaymentsWritable(totalCharges, coveredCharges);
			context.write(new Text(state), p);
		}
		
	}
	
	
	public static class PaymentsReducer extends Reducer<Text, PaymentsWritable, Text, Text> {
		
		@Override
		protected void reduce(Text key, Iterable<PaymentsWritable> values,
				Reducer<Text, PaymentsWritable, Text, Text>.Context context)
						throws IOException, InterruptedException {
			
			PaymentsWritable paymentsWritable = new PaymentsWritable();
			for(PaymentsWritable nextVal: values){
				paymentsWritable.merge(nextVal);
			}
			context.write(key, new Text(paymentsWritable.toString()));
		}
	}
	
	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
		Configuration conf = new Configuration();
  	  	Job job = new Job(conf, "hospitalanalysis");
  	  	conf.set("No of mapps", "");
  	  	conf.set("", "");
  	  	job.setJarByClass(GetPaymentDetailsByState.class);
  	  	job.setOutputKeyClass(Text.class); //For Mapper Key
	  	job.setOutputValueClass(PaymentsWritable.class); //For Mapper Value
	  	job.setMapperClass(PaymentsMapper.class);
	  	job.setReducerClass(PaymentsReducer.class);
	  	job.setInputFormatClass(TextInputFormat.class);
	  	job.setOutputFormatClass(TextOutputFormat.class);
	  	job.setNumReduceTasks(5);
	  	FileInputFormat.addInputPath(job, new Path(args[0]));
	  	FileOutputFormat.setOutputPath(job, new Path(args[1]));
    
	  	job.waitForCompletion(true);
	}
	
}
