/*
Run within the stanford NER folder
commands:
javac -cp .:stanford-ner-3.8.0.jar NERNamePlaceOrg.java
java -cp .:stanford-ner-3.8.0.jar NERNamePlaceOrg
*/

import edu.stanford.nlp.ie.AbstractSequenceClassifier;
import edu.stanford.nlp.ie.crf.*;
import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.sequences.DocumentReaderAndWriter;
import edu.stanford.nlp.util.Triple;
import java.util.*;
import java.io.*;

public class NERNamePlaceOrg
{
	public static void main(String[] args) throws Exception
	{
		String serializedClassifier = "classifiers/english.all.3class.distsim.crf.ser.gz";
		AbstractSequenceClassifier<CoreLabel> classifier = CRFClassifier.getClassifier(serializedClassifier);
		String fileName = "ArticlesRefined.csv";
		String fileLines[] = IOUtils.slurpFile(fileName).split("\n");
		PrintWriter outW = new PrintWriter(new BufferedWriter(new FileWriter("ArticlesRefinedWithNameWithPlace.csv")));
		outW.println(fileLines[0]+",Location,NamesBody,NamesHeading,Organizations");
		for(int i=1; i<fileLines.length; i++)
		{
			String fileContents = fileLines[i];
			String markedStr = classifier.classifyWithInlineXML(fileContents);
			String strs[] = new String[4];
			strs[3] = markedStr.substring(markedStr.lastIndexOf(",")+1);
			markedStr = markedStr.substring(0, markedStr.lastIndexOf(","));
			strs[2] = markedStr.substring(markedStr.lastIndexOf(",")+1);
			markedStr = markedStr.substring(0, markedStr.lastIndexOf(","));
			strs[1] = markedStr.substring(markedStr.lastIndexOf(",")+1);
			strs[0] = markedStr.substring(0, markedStr.lastIndexOf(","));
			String loc = "";
			if(strs[0].substring(0,10).equals("<LOCATION>"))
			{
				loc = strs[0].substring(10,strs[0].indexOf("</LOCATION>"));
			}
			else if(strs[0].substring(0,11).equals("\"<LOCATION>"))
			{
				loc = strs[0].substring(11,strs[0].indexOf("</LOCATION>"));
			}
			if(loc.equals(""))
			{
				String temp = strs[0].split(":")[0];
				if(temp.length()<=30)
				{
					loc = temp;
					if(loc.charAt(0)=='"')
					{
						loc = loc.substring(1);
					}
				}
			}
			
			String parts[] = strs[0].split("<PERSON>");
			String name = "";
			if(parts.length>1)
			{
				String names[] = new String[parts.length-1];
				for(int j=0; j<names.length; j++)
				{
					names[j] = parts[j+1].substring(0,parts[j+1].indexOf("</PERSON>"));
				}
				Set<String> tempSet = new HashSet<String>(Arrays.asList(names));
				String[] uniqNames = tempSet.toArray(new String[tempSet.size()]);
				name = uniqNames[0];
				for (int j=1; j<uniqNames.length; j++)
				{
					name += ";"+uniqNames[j];
				}
			}

			parts = strs[0].split("<ORGANIZATION>");
			String orgs = "";
			if(parts.length>1)
			{
				String names[] = new String[parts.length-1];
				for(int j=0; j<names.length; j++)
				{
					names[j] = parts[j+1].substring(0,parts[j+1].indexOf("</ORGANIZATION>"));
				}
				Set<String> tempSet = new HashSet<String>(Arrays.asList(names));
				String[] uniqNames = tempSet.toArray(new String[tempSet.size()]);
				orgs = uniqNames[0];
				for (int j=1; j<uniqNames.length; j++)
				{
					orgs += ";"+uniqNames[j];
				}
			}

			parts = strs[2].split("<PERSON>");
			String nameH = "";
			if(parts.length>1)
			{
				String names[] = new String[parts.length-1];
				for(int j=0; j<names.length; j++)
				{
					names[j] = parts[j+1].substring(0,parts[j+1].indexOf("</PERSON>"));
				}
				Set<String> tempSet = new HashSet<String>(Arrays.asList(names));
				String[] uniqNames = tempSet.toArray(new String[tempSet.size()]);
				nameH = uniqNames[0];
				for(int j=1; j<uniqNames.length; j++)
				{
					nameH += ";"+uniqNames[j];
				}
				String bNames[] = name.split(";");
				for(String hnm : uniqNames)
				{
					for(String bnm : bNames)
					{
						String temp[] = bnm.split(" ");
						if(temp.length>1)
						{
							for(String te : temp)
							{
								if(te.trim().equals(hnm))
								{
									nameH += ";"+bnm;
									break;
								}
							}
						}
					}
				}
			}
			outW.println(fileLines[i]+","+loc+","+name+","+nameH+","+orgs);
		}
		outW.close();
	}
}
