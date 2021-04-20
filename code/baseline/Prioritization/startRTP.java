import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.ObjectInputStream.GetField;
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.HashSet;
import java.util.ArrayList;

import javax.swing.text.AbstractDocument.LeafElement;

public class startRTP {

	public static String rootsubjectpath = "../../../subjects/experiment/"; //anonymous processing
	
	
	public static List<String> SubList = new ArrayList<String>();
	//char covMatrix[][];
	public static List<String> TestList = new ArrayList<String>();
	public static int testNum = 0;
	public static int mutantNum = 0;
	public static int columnNum = 0;
	//public static int trainingnum = 0;
	
	//read the sublist to be handled
	public static void readSubList() throws IOException{
		SubList.clear();
		FileReader fr = new FileReader(new File(rootsubjectpath + "/uselist-sc")); //anonymous processing
		BufferedReader br = new BufferedReader(fr);
		String line;
		while ((line = br.readLine()) != null){
			line = line.trim();
			SubList.add(line);
		}
		br.close();
		fr.close();
		
	}
	
	// read the coveMatrix and TestList
	public static void readMatrixandTest(String Subname) throws IOException{
		
		testNum = 0;
		mutantNum = 0;
		
		//get the test list
		
		TestList.clear();
		FileReader fr = new FileReader(new File(rootsubjectpath + Subname + "/testList"));
		//FileReader fr = new FileReader(new File(rootsubjectpath  + "/coverage/" + Subname  + "/testList"));
		BufferedReader br = new BufferedReader(fr);
		String line;
		while ((line = br.readLine()) != null){
			line = line.trim();
			TestList.add(line);
		}
		br.close();
		fr.close();
		testNum=TestList.size();
		
		
		//create the dir
		String resultDir = rootsubjectpath + Subname  + "/training/";
	//	String resultDir = rootsubjectpath  + "/result/" + Subname;
		File resultFile = new File(resultDir);
		if (!resultFile.exists())
			resultFile.mkdirs();
		
	}

	public static List<String> readTrainingTest(String filepath) throws IOException{
		List<String> traininglist = new ArrayList<String>();
		FileReader fr = new FileReader(new File(filepath));
		BufferedReader br = new BufferedReader(fr);
		String line;
		while ((line = br.readLine()) != null){
			line = line.trim();
			traininglist.add(line);
		}
		br.close();
		fr.close();
		return traininglist;
	}
	
	public static void writeresult(String writepath, int sequence[]) throws IOException{
		FileWriter fw = new FileWriter(new File(writepath));
		BufferedWriter bw = new BufferedWriter(fw);
		for(int j = 0; j < sequence.length; j++){ 
			String testname = TestList.get(sequence[j]);
			bw.write(testname);
			bw.newLine();
		}
		bw.close();
		fw.close();
		
	}

	public static char[][] getCoverageMatrix(String coverageFile){
		char[][] covMatrix = new char[testNum][];

		try{
			BufferedReader br = new BufferedReader(new FileReader(coverageFile));
			//char[][] CoverageMatrix; //Store the test case coverage information(Matrix).
			ArrayList<String> tempAl = new ArrayList<String>();
			columnNum = 0;
			String line;
			//Read all the rows from the Coverage Matrix and store then in an ArrayList for further process.
			while((line = br.readLine()) != null){
				//System.out.println(line+"\n");
				if(columnNum == 0){
					columnNum = line.length();
				}else if(columnNum != line.length()){
					System.out.println(coverageFile);
					System.out.println(columnNum + " : " + line.length());
					System.out.println("ERROR: The line from Coverage Matrix File is WORNG.\n"+line);
					System.exit(1);
				}
				tempAl.add(line);
			}


			//testCaseCovered = new ArrayList<Integer>();
			//Store the information in the ArrayList to the Array.
			for(int i=0; i<tempAl.size(); i++){
				covMatrix[i] = tempAl.get(i).toCharArray();
			}

			br.close();
		}catch(Exception e){
			e.printStackTrace();
		}

		return covMatrix;
	}

	public static float[] getTimeList(String timelistFile){
		float [] timeList = new float[testNum];
		try {
			BufferedReader br = new BufferedReader(new FileReader(timelistFile));
			String line;
			ArrayList<Float> temptime = new ArrayList<Float>();
			while((line = br.readLine()) != null){
				line = line.trim();
				temptime.add(Float.parseFloat(line));
				//this.timeList.add(Float.parseFloat(line));
			}
			for(int i=0; i<temptime.size(); i++){
				timeList[i] = temptime.get(i).floatValue();
			}
			br.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return timeList;
	}

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		
		long start, end;
		//int trainingstart = Integer.parseInt(args[1]);
		//int trainingend = Integer.parseInt(args[2]);
		
		readSubList();
		//SubList.clear();
		//SubList.add(args[0]);
		String Subname;
		for(int i = 0; i < SubList.size(); i++){
			Subname = SubList.get(i);
			readMatrixandTest(Subname);
			char covMatrix[][] = getCoverageMatrix(rootsubjectpath + Subname + '/'+ "stateMatrix.txt");
			float testTime[] = getTimeList(rootsubjectpath + Subname + '/'+ "exeTime");
 			System.out.println("sub " + Subname);


            int[] sequence;

            String gafilepath = rootsubjectpath + Subname + "/training/GAStatement";
            File gaFile = new File(gafilepath);
            if (!gaFile.exists()){
                GreedyAdditional ga = new GreedyAdditional(rootsubjectpath + Subname + '/',covMatrix);
                start = System.currentTimeMillis();
                sequence = ga.getSelectedTestSequence();
                end = System.currentTimeMillis();
                System.out.println("greedyadditional st " + (end - start));
                writeresult(rootsubjectpath + Subname + "/training/GAStatement", sequence);
                ga = null;
            }
            else{
                System.out.println(Subname + " greedyadditional st is completed!");
                }

            String tafilepath = rootsubjectpath + Subname + "/training/TAStatement";
            File taFile = new File(tafilepath);
            if (!taFile.exists()){
                TimeAdditional ta = new TimeAdditional(rootsubjectpath+Subname + '/', covMatrix,testTime);
                start = System.currentTimeMillis();
                sequence = ta.getSelectedTestSequence();
                end = System.currentTimeMillis();
                System.out.println("timeadditional st " + (end - start));
                writeresult(rootsubjectpath + Subname + "/training/TAStatement", sequence);
                ta = null;
            }
            else{
                System.out.println(Subname + " timeadditional st is completed!");
            }

            String gefilepath = rootsubjectpath + Subname + "/training/GEStatement_test";
            File geFile = new File(gefilepath);
            if (!geFile.exists()){
                Genetic ge = new Genetic(rootsubjectpath + Subname + '/',covMatrix);
                start = System.currentTimeMillis();
                sequence = ge.StartGeneration();
                end = System.currentTimeMillis();
                System.out.println("Genetic st " + (end - start));
                writeresult(rootsubjectpath + Subname + "/training/GEStatement_test", sequence);
                ge = null;
            }
            else{
                System.out.println(Subname + " Genetic st is completed!");
                }

            String tgefilepath = rootsubjectpath + Subname + "/training/TGEStatement_test";
            File tgeFile = new File(tgefilepath);
            if (!tgeFile.exists()){
                TimeGenetic tge = new TimeGenetic(rootsubjectpath+Subname + '/', covMatrix,testTime);
                start = System.currentTimeMillis();
                sequence = tge.StartGeneration();
                end = System.currentTimeMillis();
                System.out.println("timeGenetic st " + (end - start));
                writeresult(rootsubjectpath + Subname + "/training/TGEStatement_test", sequence);
                tge = null;
            }
            else{
                System.out.println(Subname + " timeGenetic st is completed!");
            }


		}		
		
	}

}
