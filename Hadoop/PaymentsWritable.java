import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

import org.apache.hadoop.io.Writable;

public class PaymentsWritable implements Writable {
	
	float totalCharges;
	float coveredCharges;
	
	public PaymentsWritable(final float totalCharges, final float coveredCharges) {
		this.totalCharges = totalCharges;
		this.coveredCharges = coveredCharges;
	}
	
	
	public PaymentsWritable() {
		// TODO Auto-generated constructor stub
	}


	@Override
	public void readFields(DataInput input) throws IOException {
		
		this.totalCharges = input.readFloat();
		this.coveredCharges = input.readFloat();
	}

	@Override
	public void write(DataOutput output) throws IOException {
		
		output.writeFloat(this.totalCharges);
		output.writeFloat(this.coveredCharges);
	}
	
	public void merge(PaymentsWritable other){
		this.totalCharges += other.totalCharges;
		this.coveredCharges += other.coveredCharges;
	}
	
	@Override
	public String toString(){
		return String.valueOf(this.totalCharges + "\t" + this.coveredCharges);
	}
	
}
