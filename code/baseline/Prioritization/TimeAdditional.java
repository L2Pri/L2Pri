
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;


public class TimeAdditional {
		String Directory;
		String matrixFile;
		//String coverageFile;
		//String timelistpath;
		//ArrayList<Float> timeList;
		float[] timeList;
		char[][] CoverageMatrix;
		final String sep = File.separator;
		char[] currentCovered; //Record the already covered statements/methods/branches.
		
		public TimeAdditional(String Directory, char[][] trainingCovMaxtrix, float[] trainingtime){
			//this.timelistpath = timeFile;
			this.Directory = Directory; //get the directory to Create a output file for Statistic Data.
			//this.matrixFile = matrixFile; //Create a new file use the same file prefix for Statistic Data.
			//this.coverageFile = Directory+this.sep+matrixFile;
			//this.timeList = new ArrayList<Float>();
			this.CoverageMatrix = trainingCovMaxtrix;
			this.timeList = trainingtime;
		}


	/*
	public void getTimeList(String timelistFile){
		try {
			BufferedReader br = new BufferedReader(new FileReader(timelistFile));	
			String line;
			while((line = br.readLine()) != null){
				line = line.trim();
				this.timeList.add(Float.parseFloat(line));
			}
			br.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	 */
		
	//Read the Coverage File and Store the value to the APBC, APDC or APSC Matrix.
	public void getCoverageMatrix(char[][] CoverageMatrix){
		try{

			int columnNum = this.CoverageMatrix[0].length;
			this.currentCovered = new char[columnNum]; //Initialized the global currentCovered.
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	
	//Calculate the number of additional '1' in the array based on the global array currentCovered.
	public int getAdditionalCoveredNumber(char[] a){
		int num = 0;
		for(int i=0; i<a.length; i++){
			if(a[i] == '1' && this.currentCovered[i] == '0'){
				num++;
			}
		}
		return num;
	}
	//Calculate the number of additional '1' in the array.
	public int getCoveredNumber(char[] a){
		int num = 0;
		for(int i=0; i<a.length; i++){
			if(a[i] == '1'){
				num++;
			}
		}
		return num;
	}
	//The main function that select the test sequence.
	public int[] getSelectedTestSequence(){
		
		this.getCoverageMatrix(this.CoverageMatrix);
		//this.getTimeList(this.timelistpath);
		
		int len = this.CoverageMatrix.length, columnNum = this.CoverageMatrix[0].length;
		int[] selectedTestSequence = new int[len];
		int[] coveredNum = new int[len];
		ArrayList<Integer> selected = new ArrayList<Integer>(); //Store the elements that are already selected.
		ArrayList<Integer> coveredZero = new ArrayList<Integer>(); //Store the elements in case  it covers 0 statement/method/branch.
		boolean containAllZeroRow = false;
		
		for(int i=0; i<len; i++){
			coveredNum[i] = this.getCoveredNumber(this.CoverageMatrix[i]);
			if(coveredNum[i] == 0){
				coveredZero.add(i);
			}
		}
		int[] originalCoveredNum = Arrays.copyOf(coveredNum, len); //Copy of coveredNum, for the remaining elements.
		this.currentCovered = new char[columnNum];
		this.clearArray(this.currentCovered);
		//System.out.println("Before:");
		//this.Print(coveredNum);
		while(selected.size() < len){
			
			int maxIndex = this.selectMax(coveredNum);
			if(maxIndex == -1){//All the statements/methods/branches are covered, then use the same algorithm for the left test cases.
				if(selected.size() == len) break;
				coveredNum = Arrays.copyOf(originalCoveredNum, len);
				maxIndex = this.selectMax(coveredNum);
				this.clearArray(this.currentCovered);
			}
			
			if(maxIndex == -1){
				/*coveredZero.add()
				System.out.println(this.coverageFile+", "+selected.size());
				this.Print(coveredNum);*/
				containAllZeroRow = true;
				System.out.println(this.Directory + " statement coverage" +" contains all 0 row.");
				break;
			}
			originalCoveredNum[maxIndex] = 0;
			//selectedTestSequence[i] = maxIndex;
			selected.add(maxIndex);
			this.mergeIntoCurrentArray(this.currentCovered, this.CoverageMatrix[maxIndex]);
			
			for(int j=0; j<len; j++){
				if(selected.contains(j)){
					coveredNum[j] = 0;
				}else{
					coveredNum[j] = this.getAdditionalCoveredNumber(this.CoverageMatrix[j]);
				}
			}
			//this.Print(this.currentCovered);
		}
		
		if(containAllZeroRow){//For this algorithm, put all the zero covered test case to the end
			for(int i=0; i<coveredZero.size(); i++){
				selected.add(coveredZero.get(i));
			}
		}
		for(int i=0; i<len; i++){
			selectedTestSequence[i] = selected.get(i);
		}
		return selectedTestSequence;
	}
	//Select the maximum number in the array and return its index.
	public int selectMax(int[] a){
		int index = -1;
		float max = 0;
		for(int i=0; i<a.length; i++){
			if(a[i]/this.timeList[i] > max){
				max = a[i]/this.timeList[i];
				index = i;
			}
		}
		
		return index;
	}
	//Merge all the '1's in the new array into the current array.
	public void mergeIntoCurrentArray(char[] current, char[] newArray){
		if(current.length != newArray.length){
			System.out.println("ERROR: mergeIntoCurrentArray: length is not equal.");
			System.exit(1);
		}
		int len = current.length;
		for(int i=0; i<len; i++){
			if(newArray[i] == '1'){
				current[i] = newArray[i];
			}
		}
	}
	//Set all elements '0' in the array.
	public void clearArray(char[] a){
		for(int i=0; i<a.length; i++){
			a[i] = '0';
		}
	}
	public void Print(char[] a){
		System.out.println("------char[] Start------");
		for(int i=0; i<a.length; i++){
			System.out.print(a[i]+",");
		}
		System.out.println("\n------char[] End------");
	}
	public void Print(int[] a){
		System.out.println("------int[] Start-----Len: "+a.length);
		for(int i=0; i<a.length; i++){
			System.out.print(a[i]+",");
		}
		System.out.println("\n------int[] End------");
	}
	/*//For Unit Test.
	public static void main(String[] args){
		GreedyAdditional ga = new GreedyAdditional("your own directory", "BranchCommonTestCasesMatrix.txt");
		ga.Print(ga.());
		
	}*/
}
