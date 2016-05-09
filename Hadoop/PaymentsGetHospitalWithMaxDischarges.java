import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class PaymentsGetHospitalWithMaxDischarges {
	
	private static int maxDischarges = 0;
	private static String hospital = "";
	public static class PaymentsMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

		@Override
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			
			String array[] = value.toString().trim().replaceAll("\\$","").split(",(?=([^\"]*\"[^\"]*\")*[^\"]*$)");
			int number = Integer.parseInt(array[8].trim());
			context.write(new Text(array[2].trim()), new IntWritable(number));
		}
	}

	public static class PaymentsReducer extends Reducer<Text, IntWritable, Text, IntWritable> {

		@Override
		protected void reduce(Text key, Iterable<IntWritable> values, Context context)
						throws IOException, InterruptedException {
			int sum = 0;
			Iterator<IntWritable> iterator = values.iterator();
			while (iterator.hasNext()) {
				IntWritable next = iterator.next();
				sum += Integer.parseInt(next.toString());
			}
			if(sum > maxDischarges){
				maxDischarges = sum;
				hospital = key.toString();
			}
		}
		
		@Override
		protected void cleanup(Context context)
				throws IOException, InterruptedException {
			hospital = "\"" + hospital + "\"";
			context.write(new Text(hospital), new IntWritable(maxDischarges));
		}
	}
	
	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
		Configuration conf = new Configuration();
  	  	Job job = new Job(conf, "hospitalanalysis");
  	  	job.setJarByClass(PaymentsGetHospitalWithMaxDischarges.class);
  	  	
  	  	job.setOutputKeyClass(Text.class);
	  	job.setOutputValueClass(IntWritable.class);
    
	  	job.setMapperClass(PaymentsMapper.class);
	  	job.setReducerClass(PaymentsReducer.class);
    
	  	job.setInputFormatClass(TextInputFormat.class);
	  	job.setOutputFormatClass(TextOutputFormat.class);
    
	  	FileInputFormat.addInputPath(job, new Path(args[0]));
	  	FileOutputFormat.setOutputPath(job, new Path(args[1]));
    
	  	job.waitForCompletion(true);
	}


}
