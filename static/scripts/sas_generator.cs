using System.IO;
using WindowsAzure;
using WindowsAzure.Storage;
using WindowsAzure.Storage.Blob;

public class sas_creater
{

	static void Main(string[] args)
	{
	    //Parse the connection string and return a reference to the storage account.
	    CloudStorageAccount storageAccount = CloudStorageAccount.Parse(CloudConfigurationManager.GetSetting("StorageConnectionString"));

	    //Create the blob client object.
	    CloudBlobClient blobClient = storageAccount.CreateCloudBlobClient();

	    //Get a reference to a container to use for the sample code, and create it if it does not exist.
	    CloudBlobContainer container = blobClient.GetContainerReference("media-file");
	    container.CreateIfNotExists();

	    //Insert calls to the methods created below here...

		Console.WriteLine("Container SAS URI: " + GetContainerSasUri(container));
		Console.WriteLine();

	    //Require user input before closing the console window.
	    Console.ReadLine();
	}

	static string GetContainerSasUri(CloudBlobContainer container)
	{
	    //Set the expiry time and permissions for the container.
	    //In this case no start time is specified, so the shared access signature becomes valid immediately.
	    SharedAccessBlobPolicy sasConstraints = new SharedAccessBlobPolicy();
	    sasConstraints.SharedAccessExpiryTime = DateTime.UtcNow.AddHours(24);
	    sasConstraints.Permissions = SharedAccessBlobPermissions.Write | SharedAccessBlobPermissions.List;

	    //Generate the shared access signature on the container, setting the constraints directly on the signature.
	    string sasContainerToken = container.GetSharedAccessSignature(sasConstraints);

	    //Return the URI string for the container, including the SAS token.
	    return container.Uri + sasContainerToken;
	}

	static string GetBlobSasUri(CloudBlobContainer container)
	{
	    //Get a reference to a blob within the container.
	    CloudBlockBlob blob = container.GetBlockBlobReference("sasblob.txt");

	    //Upload text to the blob. If the blob does not yet exist, it will be created.
	    //If the blob does exist, its existing content will be overwritten.
	    string blobContent = "This blob will be accessible to clients via a Shared Access Signature.";
	    MemoryStream ms = new MemoryStream(Encoding.UTF8.GetBytes(blobContent));
	    ms.Position = 0;
	    using (ms)
	    {
	        blob.UploadFromStream(ms);
	    }

	    //Set the expiry time and permissions for the blob.
	    //In this case the start time is specified as a few minutes in the past, to mitigate clock skew.
	    //The shared access signature will be valid immediately.
	    SharedAccessBlobPolicy sasConstraints = new SharedAccessBlobPolicy();
	    sasConstraints.SharedAccessStartTime = DateTime.UtcNow.AddMinutes(-5);
	    sasConstraints.SharedAccessExpiryTime = DateTime.UtcNow.AddHours(24);
	    sasConstraints.Permissions = SharedAccessBlobPermissions.Read | SharedAccessBlobPermissions.Write;

	    //Generate the shared access signature on the blob, setting the constraints directly on the signature.
	    string sasBlobToken = blob.GetSharedAccessSignature(sasConstraints);

	    //Return the URI string for the container, including the SAS token.
	    return blob.Uri + sasBlobToken;
	}

}