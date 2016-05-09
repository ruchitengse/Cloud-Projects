import java.io.IOException;
import java.util.Iterator;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class PaymentsGetTotalByState {
	
	public static class PaymentsMapper extends Mapper<LongWritable, Text, Text, FloatWritable> {

		@Override
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			String array[] = value.toString().trim().replaceAll("\\$","").split(",(?=([^\"]*\"[^\"]*\")*[^\"]*$)");
			Float number = Float.parseFloat(array[11].trim());
			context.write(new Text(array[5].trim()), new FloatWritable(number));
		}
	}

	public static class PaymentsReducer extends Reducer<Text, FloatWritable, Text, FloatWritable> {

		@Override
		protected void reduce(Text key, Iterable<FloatWritable> values, Context context)
						throws IOException, InterruptedException {
			float sum = 0;
			Iterator<FloatWritable> iterator = values.iterator();
			while (iterator.hasNext()) {
				FloatWritable next = iterator.next();
				sum += Float.parseFloat(next.toString());
			}
			context.write(key, new FloatWritable(sum));
		}
	}
	
	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
		Configuration conf = new Configuration();
  	  	Job job = new Job(conf, "hospitalanalysis");
  	  	job.setJarByClass(PaymentsGetTotalByState.class);
  	  	
  	  	job.setOutputKeyClass(Text.class);
	  	job.setOutputValueClass(FloatWritable.class);
    
	  	job.setMapperClass(PaymentsMapper.class);
	  	job.setReducerClass(PaymentsReducer.class);
    
	  	job.setInputFormatClass(TextInputFormat.class);
	  	job.setOutputFormatClass(TextOutputFormat.class);
    
	  	FileInputFormat.addInputPath(job, new Path(args[0]));
	  	FileOutputFormat.setOutputPath(job, new Path(args[1]));
    
	  	job.waitForCompletion(true);
	}
}