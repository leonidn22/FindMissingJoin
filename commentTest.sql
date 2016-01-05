else if @type in ('unix', 'emc', 'ntap', 'ntap_cm', 'nss') and ( charindex('//',@path) = 1 )	-- UNIXsupport full path. For unix share_name = share_path

IF @@ROWCOUNT > 0 -->> Note, proc can be called for other tables (e.g. SortedDirectoryTree). In case table exists in Hist__Archive then try to override filter in @Hist_CK_def with definition taken from sys.check_constraints

SELECT
			dirid,
			AclPermParentID,AclUnique,
			CASE
				WHEN AclUnique in (1,2) THEN 0
				WHEN aclPermParentID=ParentID THEN 1
				ELSE 2
			END as IL
		FROM dbo.SortedDirectoryTree
		WHERE posixmode=0 and entType=1

(SELECT relations.ChildDirID AS DirID FROM SDT_DerivedRelations relations
					INNER JOIN SortedDirectoryTree sdt ON sdt.DirID = relations.ChildDirID AND sdt.' + dbo.fncGetProtectedColumn(@Set) + ' = 1
													  and sdt.FilerID = @FilerID
					WHERE relations.DirID = @MailboxID
					  and relations.FilerID = @FilerID
				UNION
				SELECT @MailboxID)


UPDATE SP_UniqueRoles SET RoleIDInSite = @RoleIDInSite WHERE DirID = @SiteID AND RoleName = @RoleName and FilerID = @FilerID

inner join [vrnsDomainDB].dbo.filers f on f.filer_ID = e.FilerID and f.filer_id=@filerID

RETURN (select auth.sidID
		FROM SDT_DerivedRelations dr
		CROSS JOIN [vrnsDomainDB].dbo.filers f
		inner join [vrnsDomainDB].dbo.AuthorizerDIR auth ON dr.DirID = auth.ObjectID AND f.filer_id = auth.FilerID
		where dr.ChildDirID = @dirID
		  and dr.FilerID = @FilerID and f.filer_id = @FilerID
		UNION ALL
		select auth.sidID
		from [vrnsDomainDB].dbo.AuthorizerDIR auth
		CROSS JOIN [vrnsDomainDB].dbo.filers f
		where auth.objectID = @dirID AND f.filer_id = auth.FilerID

		)
GO
	set @sqlSTR = '
		INSERT INTO
			#SubDirsErrors
		SELECT
			tab0.DirID
		FROM
			#DirTreeTab tab0
		INNER JOIN
			SDT_DerivedRelations dr ON tab0.DirID = dr.DirID

		INNER JOIN
			TacticalErrors errs ON errs.DirID = dr.ChildDirID and errs.FilerID = @FilerID ' + @usersIn + '
		GROUP BY
			tab0.DirID'

		insert [dbo].[TMP_DCF_ResultDictionary] (FilerID, [DirID],[RuleRevisionID],[DictionaryItemID],[count])
		SELECT @FilerID, [DirID],[RuleRevisionID],[DictionaryItemID],[count]
		FROM DCF_ResultDictionary rd
		WHERE
			NOT EXISTS(SELECT * FROM [dbo].[TMP_DCF_ResultDictionary] WHERE DirId = rd.DirId AND RuleRevisionId = rd.RuleRevisionId and FilerID = @FilerID )
		AND EXISTS (SELECT * FROM TMP_DCF_Results res WHERE res.DirId = rd.DirId AND res.RuleRevisionId = rd.RuleRevisionId AND res.IsDeleted = 0 and res.FilerID = @FilerID)
		and rd.FilerID = @FilerID

	--Ready to start or running
	if exists(select 1 from FileWalkStatus where
			     AEStatus in (1,2)
			  or ErrorOnChangeStatus in (1,2)
			  or CRGraphStatus in (1,2)
			  or PublishPullWalkStatus in (1,2,5))
		return 1
	return 0
	--Get the Begining size of directory
	select @dirSize = sum(props.FilesSize)
	from SDT_properties props
	where Dirid = @dirid

	--Get the Begining size of directory
	select @dirSize = sum(props.FilesSize)
	from #SDT_properties props
	where Dirid = @dirid

	--Update share flag
	update sdt
		set flags = flags | 0x2
		from TMP_SortedDirectoryTree sdt WITH(TABLOCKX,HOLDLOCK)
		inner join SP_SiteCollections WITH(TABLOCKX,HOLDLOCK) on TMP_shares.share_DirID = sdt.DirID
		where sdt.FilerID = @FilerID and SP_SiteCollections.FilerID = @FilerID

	--Update share road
	update sdt
		set flags = flags | 0x4
		from TMP_SortedDirectoryTree sdt WITH(TABLOCKX,HOLDLOCK)
		inner join TMP_SDT_DerivedRelations dr WITH(TABLOCKX,HOLDLOCK) on dr.DirID = sdt.DirID AND dr.FilerID = sdt.FilerID
		inner join TMP_shares WITH(TABLOCKX,HOLDLOCK) on TMP_shares.share_DirID = dr.ChildDirID AND TMP_shares.filer_id = dr.FilerID
		where sdt.FilerID = @FilerID
GO

--------------------------------------------------------------------------
-- fncDFS2AccessPath
--------------------------------------------------------------------------
/*
if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[fncDFS2AccessPath]') and xtype in (N'FN', N'IF', N'TF'))
drop function [dbo].[fncDFS2AccessPath]


CREATE FUNCTION [fncDFS2AccessPath] (@DFSPath nvarchar(1536))
RETURNS
	[nvarchar] (1536)
AS
BEGIN
	declare @DirPath nvarchar(1536)
	declare @HostID int

	select @HostID = fp.hostID from [vrnsDomainDB].dbo.filers ff inner join FilerProperties fp on fp.filer_id = ff.Filer_id

	select top 1 @DirPath = dbo.fncMapPhisical2DFS(@DFSPath, dbo.fncLEN(dfs.DFSPath), ss.share_path)
	from [vrnsDomainDB].dbo.DFS_IDs dfs
	inner join dbo.shares ss
		on dfs.ShareID = ss.share_id and dfs.ShareHostID = @HostID
	where @DFSPath like dfs.DFSPath + '\%'

	RETURN @DirPath
END
*/

select top 1 @DirPath = dbo.fncMapPhisical2DFS(@DFSPath, dbo.fncLEN(dfs.DFSPath), ss.share_path)
	from [vrnsDomainDB].dbo.DFS_IDs dfs
	/*inner join dbo.shares ss*/
	
	
	JOIN dbo.DP_ExpirationDetails ExpDetails /*RELATIONS*/ ON ExpDetails.ExpirationID = R.ExpirationID
	
	